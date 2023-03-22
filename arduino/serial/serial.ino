String lastPayload = "";
char turnFace = '\0';
char turnDir = '\0';

void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, INPUT);
  pinMode(10, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    lastPayload = data;
    Serial.print("Received move list: ");
    Serial.println(data);
    Serial.print("Message received.\n");

    delay(200);

    for (unsigned int i = 0; i < data.length(); i = i + 3) {
      turnFace = data[i];
      turnDir = data[i + 1];

      while (digitalRead(9) == HIGH){}

      switch (turnFace){
        case 'U':
          digitalWrite(2, HIGH);
          break;
        case 'L':
          digitalWrite(3, HIGH);
          break;
        case 'F':
          digitalWrite(4, HIGH);
          break;
        case 'R':
          digitalWrite(5, HIGH);
          break;
        case 'B':
          digitalWrite(6, HIGH);
          break;
      }

      switch (turnDir){
        case '1':
          digitalWrite(7, HIGH);
          break;
        case '2':
          digitalWrite(7, HIGH);
          digitalWrite(8, HIGH);
          break;
        case 'P':
          digitalWrite(8, HIGH);
          break;
      }

      digitalWrite(10, HIGH);

      while (digitalRead(9) == LOW){}

      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      digitalWrite(6, LOW);
      digitalWrite(7, LOW);
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);

      
      delay(200);
    }

    digitalWrite(10, LOW);
    Serial.print('\n');
    delay(500);
  }
}
