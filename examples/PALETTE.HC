U0 PaletteLesson()
{
  I64 i;
  CDC *dc=DCAlias;
  DCFill(dc,WHITE);
  for (i=0;i<16;i++) {
    dc->color=i;
    GrRect(dc,20+(i%4)*55,
      30+(i/4)*45,45,35);
  }
  GetChar;
  DCFill(dc);
  DCDel(dc);
}
PaletteLesson;
