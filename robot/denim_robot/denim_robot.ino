// Denim pattern-drawing robot: early open-loop prototype.
// Drives a two-motor chassis in timed straight-line segments whose lengths are
// computed from body measurements, pausing between segments so each pattern
// point can be marked.

void setup() {
  pinMode(3, OUTPUT);     // right motor
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);     // left motor
  pinMode(6, OUTPUT);
}

void loop() {
float waist = 1;
float seat = 1;
float inside_leg = 2;
float rise = 4;
float knee = 2;

float a = rise - 1.5;
float d = a * 0.75;
float e = (seat * 0.125) - 0.5 ;
float f = (seat *0.25) + 1 ;
float g = e * 0.5 ;
float i = (0.25 * waist) + 1 ;
float j = 6.2 ; //half of bottom diameter
float k = 9.5 / 2 ;//half of knee diameter
float l = e * 0.75 ;
float m = 0.5 * a ;
float n = e + g - l + (0.25 * g) ;
float p = (0.25 * waist) + 1.75 ;
float r = (0.25 * seat) + 1.25;
float s = j + 0.75;
float t = k + 0.75;

float velocity = 2.1829 / 2000;  // distance per millisecond, from calibration runs
  timestop() ;
  delay(20000) ;

  forward() ;
  delay(knee / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay((inside_leg - knee) / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay(d / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay((a - d) / velocity) ;

  timestop() ;
  delay(20000) ;

  forward() ;
  delay(j / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay((j * 2) / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay(k / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay((k * 2) / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay(e / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay(g / velocity) ;

  timestop() ;
  delay(10000) ;
  
  forward() ;
  delay(f / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay(i / velocity) ;

  timestop() ;
  delay(30000) ;

// back
  forward() ;
  delay(knee / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay((inside_leg - knee) / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay(d / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay((a - d) / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay(s / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay((s * 2) / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay(t / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay((t * 2) / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay(l / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay(n / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay(m / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay(m / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay(r / velocity) ;

  timestop() ;
  delay(10000) ;

  forward() ;
  delay(p / velocity) ;

  // stop permanently once the pattern is drawn
  timestop() ;
  while (true) {}
}

//function declaration
void forward()
{
  digitalWrite(3,HIGH) ; //right forward
  digitalWrite(4,LOW) ;
  digitalWrite(5,LOW) ; //left forward
  digitalWrite(6,HIGH) ;
}

void backward()
{
  digitalWrite(3,LOW) ; // right backward
  digitalWrite(4,HIGH) ;
  digitalWrite(5,HIGH) ; // left backward
  digitalWrite(6,LOW) ;
}

void radial_right()
{
  digitalWrite(3,LOW) ; //right off
  digitalWrite(4,LOW) ;
  digitalWrite(5,LOW) ; //left forward
  digitalWrite(6,HIGH) ; 
}

void radial_left()
{
  digitalWrite(3,HIGH) ; //right forward
  digitalWrite(4,LOW) ; 
  digitalWrite(5,LOW) ; //left off
  digitalWrite(6,LOW) ;
}

void axial_right()
{
  digitalWrite(3,LOW) ; //right backward
  digitalWrite(4,HIGH) ;
  digitalWrite(5,LOW) ; //left forward
  digitalWrite(6,HIGH) ;
}

void axial_left()
{
  digitalWrite(3,HIGH) ; //right forward
  digitalWrite(4,LOW) ; 
  digitalWrite(5,HIGH) ; //left backward
  digitalWrite(6,LOW) ;
}

void timestop()
{
  digitalWrite(3,LOW) ; //right off
  digitalWrite(4,LOW) ; 
  digitalWrite(5,LOW) ; //left off
  digitalWrite(6,LOW) ;
}
