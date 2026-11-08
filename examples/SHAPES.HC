U0 Shapes()
{
  CDC *dc=DCAlias;
  DCFill(dc,WHITE);
  dc->color=BLUE;
  GrRect(dc,40,60,100,60);
  dc->color=RED;
  GrCircle(dc,190,90,30);
  dc->color=GREEN;
  GrLine(dc,40,150,220,150);
  dc->color=BLACK;
  GrPrint(dc,40,180,"Peace");
  GetChar;
  DCFill(dc);
  DCDel(dc);
}
Shapes;
