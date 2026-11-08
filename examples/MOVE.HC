I64 pilgrim_x=100;
U0 PilgrimDraw(CTask *,CDC *dc)
{
  dc->color=BLUE;
  GrRect(dc,pilgrim_x,100,12,12);
}
U0 Pilgrim()
{
  I64 key;
  SettingsPush;
  DocClear;
  Fs->draw_it=&PilgrimDraw;
  "A/D: move, Q: finish\n";
  while ((key=GetChar(,FALSE))!='q') {
    if (key=='a') pilgrim_x-=8;
    if (key=='d') pilgrim_x+=8;
    pilgrim_x=ClampI64(pilgrim_x,8,240);
  }
  SettingsPop;
}
Pilgrim;
