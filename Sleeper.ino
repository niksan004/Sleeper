#include <SD.h>
#include "RTClib.h"

const int chipSelect = 10;
const int PIR = 2;                  //Инициализация на пин за сензора за движение
const int MIC = A4;                 //Инициализация на пин за микрофона
const int number_of_readings = 600; //Променливите за четенията и забавянето са нагласени така,
const int func_delay = 100;         //че по-късно функцията да трае 1 минута
char file_name[32];                 //Инициализация на името на файла
char date_in_file[32];              //Инициализация на датата във файла

void movements_and_sound_per_min(); //Инициализация на функцията за четене на сензорите

RTC_DS1307 RTC;
File data_file;
DateTime now;

void setup(void) {
  Serial.begin(9600);
  
  RTC.begin();
  if(!RTC.isrunning()){
     Serial.println("RTC is NOT running!");
     RTC.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  if(!SD.begin(chipSelect)){
     Serial.println("Card failed, or not present");
  }  
  
  now = RTC.now();  
  sprintf(file_name, "%02d%02d%02d%02d.csv", now.month(), now.day(), now.hour(), now.minute()); //Създаване на името на файла
}

void loop() {
  now = RTC.now();  
  sprintf(date_in_file, "%4d/%02d/%02d %02d:%02d", now.year(), now.month(), now.day(), now.hour(), now.minute()); //Създаване на датата във файла

  data_file = SD.open(file_name, FILE_WRITE);
   if(data_file){
     data_file.print(date_in_file);
     data_file.print(",");
     movements_and_sound_per_min();
     data_file.close();
  }
}

void movements_and_sound_per_min(){
  //Променливи за движението
  int present_reading_movement = 0;
  float sum_of_readings_movement = 0;

  //Променливи за звука
  int present_reading_sound = 0;
  int past_reading_sound = 0;
  float sum_of_readings_sound = 0;
  int max_sound = 0;
  int diviation = 0;

  for(int i=0; i<number_of_readings; i++){
   //Отчитане на движение
   present_reading_movement = digitalRead(PIR);          
   sum_of_readings_movement += present_reading_movement;

   //Отчитане на звук
   present_reading_sound = analogRead(MIC);
   if(past_reading_sound == 0) past_reading_sound = present_reading_sound; 

   diviation = abs(present_reading_sound - past_reading_sound);
   sum_of_readings_sound += diviation;
    
   if(max_sound == 0 || diviation > max_sound) max_sound = diviation; 
    
    past_reading_sound = present_reading_sound;
    delay(func_delay);  
  }
  
  data_file.print((int)(sum_of_readings_movement / number_of_readings * 100));
  data_file.print(",");
  data_file.print((int)(sum_of_readings_sound / number_of_readings * 100));
  data_file.print(",");
  data_file.println(max_sound * 100);
}
