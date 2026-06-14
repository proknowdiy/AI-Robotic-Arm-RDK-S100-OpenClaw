#include <ESP32Servo.h>
#include <ArduinoJson.h>

#define NUM_SERVOS 4

// =====================================================
// Servo Structure
// =====================================================

struct ServoMotor {

  Servo servo;

  int pin;

  int currentAngle;

  int targetAngle;

  int minAngle;

  int maxAngle;
};

ServoMotor motors[NUM_SERVOS];

// =====================================================
// Pose Structure
// =====================================================

struct Pose {

  int base;
  int shoulder;
  int elbow;
  int gripper;
};

// =====================================================
// Poses
// =====================================================

Pose homePose = {85, 180, 180, 120};

// A
Pose hoverA = {53, 23, 98, 120};
Pose pickA  = {53, 23, 98, 70};
Pose carryA = {53, 180, 180, 70};

// B
Pose hoverB = {85, 35, 120, 120};
Pose pickB  = {85, 35, 120, 70};
Pose carryB = {85, 180, 180, 70};

// C
Pose hoverC = {123, 23, 98, 120};
Pose pickC  = {123, 23, 98, 70};
Pose carryC = {123, 180, 180, 70};

// LEFT Position

Pose hoverLeft = {10, 60, 120, 70};
Pose dropLeft  = {10, 60, 120, 120};

// RIGHT Position

Pose hoverRight = {165, 60, 120, 70};
Pose dropRight  = {165, 60, 120, 120};

// =====================================================

unsigned long lastMoveTime = 0;

bool cubePicked = false;

const int moveInterval = 15;

// =====================================================
// Setup
// =====================================================

void setup() {

  Serial.begin(115200);

  delay(2000);

  setupMotor(0, 0, 90, 0, 180);      // Base
  setupMotor(1, 1, 90, 0, 180);      // Shoulder
  setupMotor(2, 4, 90, 0, 180);      // Elbow
  setupMotor(3, 6, 60, 30, 120);     // Gripper

  moveToPose(homePose);

  Serial.println("Robot Ready");
}

// =====================================================

void loop() {

  handleSerial();

  updateMotors();
}

// =====================================================
// Setup Motor
// =====================================================

void setupMotor(
  int index,
  int pin,
  int startAngle,
  int minAngle,
  int maxAngle
) {

  motors[index].pin = pin;

  motors[index].currentAngle = startAngle;

  motors[index].targetAngle = startAngle;

  motors[index].minAngle = minAngle;

  motors[index].maxAngle = maxAngle;

  motors[index].servo.attach(pin);

  motors[index].servo.write(startAngle);
}

// =====================================================
// Motion Functions
// =====================================================

void moveToPose(Pose pose) {

  setMotorTarget(0, pose.base);
  setMotorTarget(1, pose.shoulder);
  setMotorTarget(2, pose.elbow);
  setMotorTarget(3, pose.gripper);

  waitForMotionComplete();

  delay(300);
}

// =====================================================

void waitForMotionComplete() {

  bool moving = true;

  while (moving) {

    updateMotors();

    moving = false;

    for (int i = 0; i < NUM_SERVOS; i++) {

      if (motors[i].currentAngle != motors[i].targetAngle) {

        moving = true;
      }
    }
  }
}

// =====================================================

void pickCube(char source) {

  switch (source) {

    case 'A':

      moveToPose(hoverA);
      moveToPose(pickA);
      moveToPose(carryA);

      break;

    case 'B':

      moveToPose(hoverB);
      moveToPose(pickB);
      moveToPose(carryB);

      break;

    case 'C':

      moveToPose(hoverC);
      moveToPose(pickC);
      moveToPose(carryC);

      break;
  }

  cubePicked = true;
}

// =====================================================

void dropCube(String destination) {

  if (!cubePicked) {

    Serial.println("ERROR:NO_CUBE");

    return;
  }

  if (destination == "LEFT") {

    moveToPose(hoverLeft);
    moveToPose(dropLeft);
  }

  else if (destination == "RIGHT") {

    moveToPose(hoverRight);
    moveToPose(dropRight);
  }

  cubePicked = false;

  moveToPose(homePose);
}

// =====================================================

void moveCube(char source, String destination) {

  pickCube(source);

  dropCube(destination);
}

// =====================================================

void setMotorTarget(int index, int angle) {

  angle = constrain(
    angle,
    motors[index].minAngle,
    motors[index].maxAngle
  );

  motors[index].targetAngle = angle;
}

// =====================================================

void updateMotors() {

  if (millis() - lastMoveTime < moveInterval) {
    return;
  }

  lastMoveTime = millis();

  for (int i = 0; i < NUM_SERVOS; i++) {

    if (motors[i].currentAngle < motors[i].targetAngle) {

      motors[i].currentAngle++;

      motors[i].servo.write(motors[i].currentAngle);
    }

    else if (motors[i].currentAngle > motors[i].targetAngle) {

      motors[i].currentAngle--;

      motors[i].servo.write(motors[i].currentAngle);
    }
  }
}

// =====================================================
// JSON Handler
// =====================================================

void handleSerial() {

  if (!Serial.available()) {
    return;
  }

  String json = Serial.readStringUntil('\n');

  StaticJsonDocument<256> doc;

  DeserializationError error =
      deserializeJson(doc, json);

  if (error) {

    Serial.println("JSON Error");

    return;
  }

  // -------------------------------------------------
  // Direct Servo Control
  // -------------------------------------------------

  if (doc["cmd"] == "move") {

    setMotorTarget(0, doc["base"]);
    setMotorTarget(1, doc["shoulder"]);
    setMotorTarget(2, doc["elbow"]);
    setMotorTarget(3, doc["gripper"]);

    return;
  }

  // -------------------------------------------------
  // Motion API
  // -------------------------------------------------

  const char* action = doc["action"];

  if (!action) {
    return;
  }

  if (strcmp(action, "home") == 0) {

    moveToPose(homePose);

    Serial.println("Done");
  }

  else if (strcmp(action, "pick_cube") == 0) {

    char source =
      doc["source"].as<const char*>()[0];

    pickCube(source);

    Serial.println("Done");
  }

  else if (strcmp(action, "drop_cube") == 0) {

    if (!cubePicked) {

      Serial.println("ERROR:NO_CUBE");

      return;
    }

    String destination =
      doc["destination"].as<String>();

    dropCube(destination);

    Serial.println("Done");
  }

  else if (strcmp(action, "move_cube") == 0) {

    char source =
      doc["source"].as<const char*>()[0];

    String destination =
      doc["destination"].as<String>();

    moveCube(source, destination);

    Serial.println("Done");
  }
  else if (strcmp(action, "status") == 0) {

    StaticJsonDocument<64> reply;

    reply["holding_cube"] = cubePicked;

    serializeJson(reply, Serial);

    Serial.println();
  }
}