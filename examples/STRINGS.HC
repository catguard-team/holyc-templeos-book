U0 Words()
{
  U8 text[16];
  StrCpy(text,"PEACE");
  "Before: %s\n",text;
  "Length: %d\n",StrLen(text);
  "First: %c\n",text[0];
  text[0]='p';
  "After: %s\n",text;
}
Words;
