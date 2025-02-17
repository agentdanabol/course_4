import {
  to = yandex_compute_instance.testvm
  id = "epdg7bc727b38hlnqb42"
}

resource "yandex_compute_instance" "testvm" {
  name                      = "testvm"
  platform_id               = "standard-v3"
  allow_stopping_for_update = true

  resources {
    cores  = 2
    memory = 4
  }
          
  scheduling_policy {
    preemptible = true
  }
  
  boot_disk {
    disk_id = yandex_compute_disk.testvm.id
    auto_delete = false
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.dev.id
  }
}