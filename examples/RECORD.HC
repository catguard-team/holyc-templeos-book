class CLamp
{
  I64 x,y;
  Bool lit;
};
U0 RecordLesson()
{
  CLamp lamp;
  lamp.x=120;
  lamp.y=80;
  lamp.lit=TRUE;
  "Lamp: %d,%d lit=%d\n",
    lamp.x,lamp.y,lamp.lit;
}
RecordLesson;
