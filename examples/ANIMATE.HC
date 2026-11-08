I64 glow_x=30;
U0 GlowDraw(CTask *,CDC *dc)
{
  dc->color=YELLOW;
  GrCircle(dc,glow_x,90,12);
}
U0 Glow()
{
  I64 i;
  SettingsPush;
  DocClear;
  Fs->draw_it=&GlowDraw;
  for (i=0;i<60;i++) {
    glow_x=30+i*3;
    Sleep(30);
  }
  SettingsPop;
}
Glow;
