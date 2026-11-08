U0 SixNumbers()
{
  I64 i,value;
  for (i=0;i<6;i++) {
    value=1+RandU32%6;
    "%d\n",value;
  }
}
SixNumbers;
