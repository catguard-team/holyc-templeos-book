U0 HeapLesson()
{
  I64 i;
  I64 *values=MAlloc(4*sizeof(I64));
  if (!values)
    return;
  for (i=0;i<4;i++)
    values[i]=i*i;
  "Last: %d\n",values[3];
  Free(values);
  values=NULL;
}
HeapLesson;
