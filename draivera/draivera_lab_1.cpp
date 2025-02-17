#include <iostream>

int main() {
    unsigned short port = 0x2F8; // COM1
    unsigned char value = 0xAA;  // Тестовое значение для записи

    std::cout << "Запись значения 0xAA в порт 0x2F8 (COM1)" << std::endl;

    // Вставка ассемблерного кода
    asm volatile (
        "outb %0, %1"        // Команда outb: записать AL в порт DX
        :                    // Нет выходных операндов
        : "Nd" (port)  // Входные операнды: данные (AL) и порт (DX)
    );

    return 0;
}
