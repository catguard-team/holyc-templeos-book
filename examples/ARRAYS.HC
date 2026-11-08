U0 Seeds()
{
  I64 count[4];
  count[0]=2;
  count[1]=3;
  count[2]=5;
  count[3]=7;
  I64 i,total=0;
  for (i=0;i<4;i++) {
    "Bed %d: %d\n",i,count[i];
    total+=count[i];
  }
  "All seeds: %d\n",total;
}
Seeds;
