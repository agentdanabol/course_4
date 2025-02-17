# Local values
locals {
  boot_disk_name      = var.boot_disk_name != null ? var.boot_disk_name : "${var.name_prefix}-boot-disk" 
  linux_vm_name       = var.linux_vm_name != null ? var.linux_vm_name : "${var.name_prefix}-linux-vm"
  vpc_network_name    = var.vpc_network_name != null ? var.vpc_network_name : "${var.name_prefix}-private"
} 

# Создание VPC и подсети
resource "yandex_vpc_network" "this" {
  name = local.vpc_network_name
}

resource "yandex_vpc_subnet" "private" {
  for_each = var.zones

  name           = keys(var.subnets)[index(tolist(var.zones), each.value)]
  zone           = each.value
  v4_cidr_blocks = var.subnets[each.value]
  network_id     = yandex_vpc_network.this.id
}

resource "yandex_vpc_address" "this" {
  for_each = var.zones

  name = length(var.zones) > 1 ? "${local.linux_vm_name}-address-${substr(each.value, -1, 0)}" : "${local.linux_vm_name}-address"
  external_ipv4_address {
    zone_id = each.value
  }
} 

# Создание диска и виртуальной машины
resource "yandex_compute_disk" "boot_disk" {
  for_each = var.zones

  name     = length(var.zones) > 1 ? "${local.boot_disk_name}-${substr(each.value, -1, 0)}" : local.boot_disk_name
  zone     = each.value
  image_id = var.image_id

  type = var.instance_resources.disk.disk_type
  size = var.instance_resources.disk.disk_size
}

resource "random_string" "bucket_name" {
  length  = 8
  special = false
  upper   = false
} 

resource "yandex_compute_instance" "this" {
  for_each = var.zones

  name                      = length(var.zones) > 1 ? "${local.linux_vm_name}-${substr(each.value, -1, 0)}" : local.linux_vm_name
  allow_stopping_for_update = true
  platform_id               = var.instance_resources.platform_id
  zone                      = each.value

  resources {
    cores  = var.instance_resources.cores
    memory = var.instance_resources.memory
  }

  boot_disk {
    disk_id = yandex_compute_disk.boot_disk[each.value].id
  }

  network_interface {
    subnet_id      = yandex_vpc_subnet.private[each.value].id
    nat            = true
    nat_ip_address = yandex_vpc_address.this[each.value].external_ipv4_address[0].address
  }

  metadata = {
    user-data = templatefile("cloud-init.yaml.tftpl", {
        instance_connect_string = yandex_vpc_address.this[each.value].external_ipv4_address[0].address,
        instance_cpu = var.instance_resources.cores,
        instance_memory = var.instance_resources.memory
        # ydb_connect_string = yandex_ydb_database_serverless.this.ydb_full_endpoint,
        # bucket_domain_name = yandex_storage_bucket.this.bucket_domain_name
    })
  }
  
}

# Создание Yandex Managed Service for YDB
#resource "yandex_ydb_database_serverless" "this" {
#  name = "test-ydb-serverless"
#}

# Создание сервисного аккаунта 
#resource "yandex_iam_service_account" "bucket" {
#  name = "bucket-sa"
#}

# Назначение роли сервисному аккаунту
#resource "yandex_resourcemanager_folder_iam_member" "storage_editor" {
#  folder_id = "<folder_id>"
#  role      = "storage.editor"
#  member    = "serviceAccount:${yandex_iam_service_account.bucket.id}"
#}

# Создание статического ключа доступа
#resource "yandex_iam_service_account_static_access_key" "this" {
#  service_account_id = yandex_iam_service_account.bucket.id
#  description        = "static access key for object storage"
#}

# Создание бакета 
#resource "yandex_storage_bucket" "this" {
#  bucket     = "test-s3-bucket-fm3oijfiwf3oro23dffoi32"
#  access_key = yandex_iam_service_account_static_access_key.this.access_key
#  secret_key = yandex_iam_service_account_static_access_key.this.secret_key
#  
#  depends_on = [ yandex_resourcemanager_folder_iam_member.storage_editor ]
#}