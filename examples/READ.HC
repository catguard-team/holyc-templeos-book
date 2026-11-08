U0 ReadNote()
{
  I64 size=0,i;
  U8 *text=FileRead("NOTE.TXT",&size);
  if (!text) {
    "Run SAVE.HC first.\n";
    return;
  }
  "Read bytes: %d\n",size;
  for (i=0;i<size;i++)
    "%c",text[i];
  Free(text);
}
ReadNote;
