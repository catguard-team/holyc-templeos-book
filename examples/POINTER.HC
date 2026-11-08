U0 PointerLesson()
{
  I64 lamp=3;
  I64 *address=&lamp;
  "Before: %d\n",lamp;
  *address=7;
  "After: %d\n",lamp;
}
PointerLesson;
