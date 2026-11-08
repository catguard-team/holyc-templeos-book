U0 SayHello()
{
  U8 *name=GetStr("Your name: ");
  if (name) {
    "Hello, %s.\n",name;
    Free(name);
  }
}
SayHello;
