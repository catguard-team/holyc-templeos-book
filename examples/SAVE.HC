U0 SaveNote()
{
  U8 *text="A small work, made with care.\n";
  I64 size=StrLen(text);
  FileWrite("NOTE.TXT",text,size);
  "Requested bytes: %d\n",size;
}
SaveNote;
