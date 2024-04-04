# **My first cpp game development try**

```c++
    #include<graphics.h>
    #include<iostream>
    
    int main()
    {
        initgraph(1280, 720);
    
        int x = 300;
        int y = 300;
    
        while (true)
        {
            ExMessage msg;
            while (peekmessage(&msg))
            {
                if (msg.message == WM_MOUSEMOVE)
                {
                    x = msg.x;
                    y = msg.y;
                }
            }
            cleardevice();
            solidcircle(x, y, 100);
            FlushBatchDraw();
        }
        return 0;
    }
```

This cpp code implement a window plotting a circle following your mouser movement.
