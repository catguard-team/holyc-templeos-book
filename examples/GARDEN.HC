#define GARDEN_COUNT 7
I64 garden_lit=0;

U0 GardenDraw(CTask *task,CDC *dc)
{
  I64 i,x,y;
  I64 width=task->pix_width;
  I64 height=task->pix_height;
  dc->color=BLUE;
  GrPrint(dc,16,20,"A SMALL OFFERING");
  GrPrint(dc,16,40,"1-7: lamps   R: reset   Q: leave");
  y=height/2;
  for (i=0;i<GARDEN_COUNT;i++) {
    x=(i+1)*width/(GARDEN_COUNT+1);
    dc->color=LTGRAY;
    GrRect(dc,x-6,y,13,40);
    if (garden_lit & (1<<i))
      dc->color=YELLOW;
    else
      dc->color=DKGRAY;
    GrCircle(dc,x,y-12,9);
    dc->color=BLUE;
    GrPrint(dc,x-4,y+50,"%d",i+1);
  }
  dc->color=BLUE;
  if (garden_lit==127)
    GrPrint(dc,16,height-35,"Peace be with you.");
}

U0 Garden()
{
  I64 key;
  SettingsPush;
  DocClear;
  Fs->draw_it=&GardenDraw;
  while ((key=GetChar(,FALSE))!='q') {
    if ('1'<=key<='7')
      garden_lit^=1<<(key-'1');
    if (key=='r')
      garden_lit=0;
  }
  SettingsPop;
}
Garden;
