#define AN A0

int valor;
int echantillon=50;
unsigned long somme=0;
unsigned long moyenne=0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int i=0;i<echantillon;i++)
  {
    valor=analogRead(AN);
    somme=somme+valor;
    moyenne=somme/echantillon;
    //delay(10);
}
somme=0;
//Serial.print("Valor=");
Serial.println(moyenne);
if (valor>250)
{
  //Serial.println("La calidad del aire es mala");  
} else {
  //Serial.println("La calidad del aire es buena");
}
//delay(10);

}
