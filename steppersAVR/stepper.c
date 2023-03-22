#include <avr/io.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define F_CPU 16000000
#define motor_delay 60
#define move_delay 10

#include <util/delay.h>

static char solution[1000] = "Hello";

void moveU()
{
  PORTC &= ~0x1;
  for (int i = 0; i < 50; i++)
  {
    PORTB |= 0x1; // PORTB0 = U
    _delay_ms(1);
    PORTB &= ~0x1; // PORTB0
    _delay_ms(1);
  }
  PORTC |= 0x1;
  _delay_ms(motor_delay);
}
void moveR()
{
  PORTC &= ~0x2;
  for (int i = 0; i < 50; i++)
  {
    PORTB |= 0x2; // PORTB1 = R
    _delay_ms(1);
    PORTB &= ~0x2; // PORTB1
    _delay_ms(1);
  }
  PORTC |= 0x2;
  _delay_ms(motor_delay);
}
void moveL()
{
  PORTC &= ~0x4;
  for (int i = 0; i < 50; i++)
  {
    PORTB |= 0x4; // PORTB2 = L
    _delay_ms(1);
    PORTB &= ~0x4; // PORTB2
    _delay_ms(1);
  }
  PORTC |= 0x4;
  _delay_ms(motor_delay);
}
void moveB()
{
  PORTC &= ~0x8;
  for (int i = 0; i < 50; i++)
  {
    PORTB |= 0x8; // PORTB3 = B
    _delay_ms(1);
    PORTB &= ~0x8; // PORTB3
    _delay_ms(1);
  }
  PORTC |= 0x8;
  _delay_ms(motor_delay);
}
void moveF()
{
  PORTC &= ~0x10;
  for (int i = 0; i < 50; i++)
  {
    PORTB |= 0x10; // PORTB4 = F
    _delay_ms(1);
    PORTB &= ~0x10; // PORTB0
    _delay_ms(1);
  }
  PORTC |= 0x10;
  _delay_ms(motor_delay);
}

void moveUP()
{
  PORTB |= 0x20; // 10 0000
  moveU();
  PORTB &= ~0x20; 
}
void moveRP()
{
  PORTB |= 0x20; 
  moveR();
  PORTB &= ~0x20; 
}
void moveLP()
{
  PORTB |= 0x20; 
  moveL();
  PORTB &= ~0x20;
}
void moveBP()
{
  PORTB |= 0x20; 
  moveB();
  PORTB &= ~0x20; 
}
void moveFP()
{
  PORTB |= 0x20; 
  moveF();
  PORTB &= ~0x20;
}

void moveU2()
{
  PORTC &= ~0x1;
  for (int i = 0; i < 100; i++)
  {
    PORTB |= 0x1; // PORTB0 = U
    _delay_ms(1);
    PORTB &= ~0x1; // PORTB0
    _delay_ms(1);
  }
  PORTC |= 0x1;
  _delay_ms(motor_delay);
}
void moveR2()
{
  PORTC &= ~0x2;
  for (int i = 0; i < 100; i++)
  {
    PORTB |= 0x2; // PORTB1 = R
    _delay_ms(1);
    PORTB &= ~0x2; 
    _delay_ms(1);
  }
  PORTC |= 0x2;
  _delay_ms(motor_delay);
}
void moveL2()
{
  PORTC &= ~0x4;
  for (int i = 0; i < 100; i++)
  {
    PORTB |= 0x4; // PORTB2 = L
    _delay_ms(1);
    PORTB &= ~0x4; 
    _delay_ms(1);
  }
  PORTC |= 0x4;
  _delay_ms(motor_delay);
}
void moveB2()
{
  PORTC &= ~0x8;
  for (int i = 0; i < 100; i++)
  {
    PORTB |= 0x8; // PORTB3 = B
    _delay_ms(1);
    PORTB &= ~0x8; 
    _delay_ms(1);
  }
  PORTC |= 0x8;
  _delay_ms(motor_delay);
}
void moveF2()
{
  PORTC &= ~0x10;
  for (int i = 0; i < 100; i++)
  {
    PORTB |= 0x10; // PORTB4 = F
    _delay_ms(1);
    PORTB &= ~0x10; 
    _delay_ms(1);
  }
  PORTC |= 0x10;
  _delay_ms(motor_delay);
}

void readMoves() {
  // U L F R B
  // U R L B F
  //PD0-PD4 == face 0001 1111
  //PD5-PD6 == turn 0110 0000
  
  int i = 0;
  solution[2] = "Hello";

  while ((PIND & 0x7F) >= 1) {
    if ((PIND & 0x1) == 0x1) {       //01 00001  0x21
      solution[i] = 'U';
      i++;
      if ((PIND & 0x60) == 0x20) {          // 010 0000
        solution[i] = '1';
      }
      else if ((PIND & 0x60) == 0x40) {     // 100 0000
        solution[i] = 'P';
      }
      else if ((PIND & 0x60) == 0x60) {     // 110 0000
        solution[i] = '2';
      }
      i++;
    }
    else if ((PIND & 0x2) == 0x2) {
      solution[i] = 'R';
      i++;
      if ((PIND & 0x60) == 0x20) {          // 010 0000
        solution[i] = '1';
      }
      else if ((PIND & 0x60) == 0x40) {     // 100 0000
        solution[i] = 'P';
      }
      else if ((PIND & 0x60) == 0x60) {     // 110 0000
        solution[i] = '2';
      }
      i++;
    }
    else if ((PIND & 0x4) == 0x4) {
      solution[i] = 'L';
      i++;
      if ((PIND & 0x60) == 0x20) {          // 010 0000
        solution[i] = '1';
      }
      else if ((PIND & 0x60) == 0x40) {     // 100 0000
        solution[i] = 'P';
      }
      else if ((PIND & 0x60) == 0x60) {     // 110 0000
        solution[i] = '2';
      }
      i++;
    }
    else if ((PIND & 0x8) == 0x8) {
      solution[i] = 'B';
      i++;
      if ((PIND & 0x60) == 0x20) {          // 010 0000
        solution[i] = '1';
      }
      else if ((PIND & 0x60) == 0x40) {     // 100 0000
        solution[i] = 'P';
      }
      else if ((PIND & 0x60) == 0x60) {     // 110 0000
        solution[i] = '2';
      }
      i++;
    }
    else if ((PIND & 0x10) == 0x10) {
      solution[i] = 'F';
      i++;
      if ((PIND & 0x60) == 0x20) {          // 010 0000
        solution[i] = '1';
      }
      else if ((PIND & 0x60) == 0x40) {     // 100 0000
        solution[i] = 'P';
      }
      else if ((PIND & 0x60) == 0x60) {     // 110 0000
        solution[i] = '2';
      }
      i++;
    }
    solution[i] = ',';
    i++;
    PORTC |= 0x20;
    _delay_ms(move_delay);
    PORTC &= ~0x20;
    _delay_ms(move_delay);
  }
  solution[i+1] = '\0';
}

int main(void)
{
  // Arduino digital pin 8 (pin 0 of PORTB) for output
  DDRB = 0x3F; PORTB = 0x00; // PORTB0
  DDRC = 0x2F; PORTC = 0x00;
  DDRD = 0x00; PORTD = 0x00;

  /* ************************************************************************************************************ */

  //char solution[] = "L1,U1,LP,UP";
  //char solution[] = "FP,BP,RP,L2,U2,LP,B1,UP,R1,BP,R1,LP,B1,L1,UP,F1,U1,FP,L1,U1,LP,U1,U1,R1,UP,RP,B1,U1,BP,U1,L1,U2,LP,UP,L1,U1,LP,U2,UP,LP,U1,L1,U1,F1,UP,FP,U1,U1,B1,UP,BP,UP,RP,U1,R1,U2,U1,L1,UP,LP,UP,BP,U1,B1,UP,UP,FP,U1,F1,U1,R1,UP,RP,U1,R1,U2,R2,UP,R2,UP,R2,U2,R1,U1,U1,U1,U2,R1,UP,R1,U1,R1,U1,R1,UP,RP,UP,R2,R2,F2,RP,BP,R1,F2,RP,B1,RP,U2,U1,U1,U1";

  int length = 0;

  /*
  PORTB0 / PIN 8 == U
  PORTB1 / PIN 9 == R
  PORTB2 / PIN 10 == L
  PORTB3 / PIN 11 == B
  PORTB4 / pin 12 == F
  */

  while (1) {

    PORTC = PORTC | 0x1F;

    if ((PIND & 0B10000000) > 0) {

      readMoves();
      length = strlen(solution);
      
      for (int i = 0; i < length; i += 3) {

        char nextmove[] = {'U', 'P', '\0'};

        nextmove[0] = solution[i];
        nextmove[1] = solution[i + 1];

        if (nextmove[0] == 'U' && nextmove[1] == '1') {
          moveU();
        }
        else if (nextmove[0] == 'R' && nextmove[1] == '1') {
          moveR();
        }
        else if (nextmove[0] == 'L' && nextmove[1] == '1') {
          moveL();
        }
        else if (nextmove[0] == 'B' && nextmove[1] == '1') {
          moveB();
        }
        else if (nextmove[0] == 'F' && nextmove[1] == '1') {
          moveF();
        }
        else if (nextmove[0] == 'U' && nextmove[1] == 'P') {
          moveUP();
        }
        else if (nextmove[0] == 'R' && nextmove[1] == 'P') {
          moveRP();
        }
        else if (nextmove[0] == 'L' && nextmove[1] == 'P') {
          moveLP();
        }
        else if (nextmove[0] == 'B' && nextmove[1] == 'P') {
          moveBP();
        }
        else if (nextmove[0] == 'F' && nextmove[1] == 'P') {
          moveFP();
        }
        else if (nextmove[0] == 'U' && nextmove[1] == '2') {
          moveU2();
        }
        else if (nextmove[0] == 'R' && nextmove[1] == '2') {
          moveR2();
        }
        else if (nextmove[0] == 'L' && nextmove[1] == '2') {
          moveL2();
        }
        else if (nextmove[0] == 'B' && nextmove[1] == '2') {
          moveB2();
        }
        else if (nextmove[0] == 'F' && nextmove[1] == '2') {
          moveF2();
        }
        else {
          printf("Move Read ERROR\n");
        }
      }
    }
  }
    return 0;
}