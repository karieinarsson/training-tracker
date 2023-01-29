
#include <MPU6050_light.h>
#include <Wire.h>
#include <LinkedList.h>
#include "BluetoothSerial.h"


#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

MPU6050 sensor(Wire);

float accX, accY, accZ;
float angleX, angleY, angleZ;
float aX, aY, aZ;

float startAcc = 0.20; // TODO
float stopVal = 0.05;
int maxCount = 100;

int timer = 0;

String accData;

BluetoothSerial SerialBT;

void setup() {
  
  Serial.begin(115200);
  SerialBT.begin("BauriTest"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
  
  Wire.begin();
  sensor.begin();
  Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  sensor.calcOffsets(true, true);
  Serial.println("Done!\n");
  
}

void loop() {
  delay(20);
  
  sensor.update();

  accX = sensor.getAccX();
  accY = sensor.getAccY();
  accZ = sensor.getAccZ();

  angleX  = sensor.getAngleX() * PI/180;
  angleY  = sensor.getAngleY() * PI/180;
  angleZ  = sensor.getAngleZ() * PI/180;

  aZ = accY * sin(angleX) - accX * sin(angleY) + accZ * cos(angleX) * cos(angleY) - 1;

  if (abs(aZ) > startAcc) 
  {
    int count = 0;
    
    LinkedList<float> xList = LinkedList<float>();
    LinkedList<float> yList = LinkedList<float>();
    LinkedList<float> zList = LinkedList<float>();

    int t = millis();
    while(true)
    { 
      timer = millis();
      while(timer%2 != 0)
        timer = millis();
      
      sensor.update();
      
      accX = sensor.getAccX();
      accY = sensor.getAccY();
      accZ = sensor.getAccZ();
      
      angleX  = sensor.getAngleX() * PI/180;
      angleY  = sensor.getAngleY() * PI/180;
      angleZ  = sensor.getAngleZ() * PI/180;
      
      aX = accZ * sin(angleY) * cos(angleZ) + accX * cos(angleY) * cos(angleZ);
      aY = accZ * sin(angleX) * cos(angleZ) - accY * cos(angleX) * cos(angleZ);
      aZ = accY * sin(angleX) - accX * sin(angleY) + accZ * cos(angleX) * cos(angleY) - 1;

      xList.add(aX);
      yList.add(aY);
      zList.add(aZ);

      if (abs(aZ) < stopVal)
        count++;
      else
        count = 0;

      if (count > maxCount)
        break;
    }

    int t2 = millis() - t;
    
    // Sending all data
    int listSize = xList.size();
    
    for (int h = 0; h < listSize - maxCount; h++) 
    {
      accData = String(xList.get(h)) + String(", ") + String(yList.get(h)) + String(", ") + String(zList.get(h));
      SerialBT.println(accData);
    
    }
    
    SerialBT.println(t2);
    SerialBT.println(listSize);
    SerialBT.println("Done");
  }
}
