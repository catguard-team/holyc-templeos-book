U0 LightDrawing(CTask *task,CDC *dc)
{
  I64 x=task->pix_width/2;
  I64 y=task->pix_height/2;
  dc->color=YELLOW;
  GrCircle(dc,x,y,45);
  dc->color=BLUE;
  GrRect(dc,x-4,y-30,9,60);
  GrRect(dc,x-24,y-15,49,8);
}
U0 LightWindow()
{
  SettingsPush;
  DocClear;
  Fs->draw_it=&LightDrawing;
  GetChar;
  SettingsPop;
}
LightWindow;
