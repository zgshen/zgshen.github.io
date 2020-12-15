---
title: opencv简单的彩色图像灰度化和二值化（学习笔记）
categories: 技术
tags: 其他
date: 2015-05-04
---
  图像的灰度化即是将彩色图像转化成为灰度图像的过程成为图像的灰度化处理。彩色图像中的每个像素的颜色有R、G、B三个分量决定，而每个分量有255中值可取，这样一个像素点可以有1600多万（255*255*255）的颜色的变化范围。而灰度图像是R、G、B三个分量相同的一种特殊的彩色图像，其一个像素点的变化范围为255种，所以在数字图像处理种一般先将各种格式的图像转变成灰度图像以使后续的图像的计算量变得少一些。灰度图像的描述与彩色图像一样仍然反映了整幅图像的整体和局部的色度和亮度等级的分布和特征。图像的灰度化处理可用两种方法来实现。
   图像的二值化是将图像上的像素点的灰度值设置为0或255，也就是将整个图像呈现出明显的黑白效果。要对RGB彩色图像进行二值化一般首先要对图像进行灰度化处理。
<!--more-->
例子  
```c
    #include "cv.h"
    #include "highgui.h"
    #include <cvaux.h>

    int main(int argc, char *argv[])
    {
        IplImage* img;
        IplImage* img0;
        IplImage* img1;

        img = cvLoadImage("test.jpg");//默认初始图像放在工程文件下
        //IplImage* img1 = img;

        if (NULL == img)
            return 0;

//灰度化操作
        img0 = cvCreateImage(cvGetSize(img),IPL_DEPTH_8U,1);//申请一段内存
        cvCvtColor(img,img0,CV_BGR2GRAY);
//图像数据复制
        img1 = cvCreateImage(cvGetSize(img),IPL_DEPTH_8U,1);//申请一段内存
        cvCopy(img0, img1, NULL);//数据复制，若直接赋值相当指针指向同一地址会对原本img0操作


//二值化操作
        int height = img1->height;
        int width = img1->width;
        int step = img1->widthStep;
        int channels = img1->nChannels;
        uchar *data = (uchar*)img1->imageData;

        for(int i=0;i != height; ++ i)
        {
         for(int j=0;j != width; ++ j)
         {
             for(int k=0;k != channels; ++ k)
             {
                 if(data[i*step+j*channels+k]<128)
                  data[i*step+j*channels+k]=0;//255-data[i*step+j*channels+k];
                  else
                  data[i*step+j*channels+k]=255;//255-data[i*step+j*channels+k];
             }
         }
        }
//创建窗口、显示图像、销毁图像、释放图像
        cvNamedWindow( "test1", 0 );
        cvShowImage("test1", img0);

        cvNamedWindow( "test", 0 );
        cvShowImage("test", img1);

        cvWaitKey(0);

        cvDestroyWindow( "test1" );
        cvDestroyWindow( "test" );

        cvReleaseImage( &img0 );
        cvReleaseImage( &img1 );

        return 0;
    }
```


