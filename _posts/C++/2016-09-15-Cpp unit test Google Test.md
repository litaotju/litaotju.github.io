---
layout: post
title: Cpp Unit Test Google Test
description: 
category: C++
tags: 
---
{% include JB/setup %}

# C++单元测试框架

单元测试是应该是针对程序的最小单位，函数的测试。测试框架则是一种比较好用的测试基础设施。googletest是一个开源的C++单元测试框架。
详情可见[github googletest](https://github.com/google/googletest).

测试框架的使用可参照官方文档 和 [googletest 探究](http://www.cnblogs.com/coderzh/archive/2009/04/11/1433744.html)

# Google Test Minimal Demo

``` c
    #include "gtest/gtest.h"

    int add(int a, int b) {
        return a + b;
    }

    TEST(TestAdd, TestAddCase)
    {
        // This will successful
        EXPECT_EQ(2, add(1, 1));
        // This will be failed
        EXPECT_EQ(2, add(2, 1));
    }


    int main(int argc, char *argv[]) {
        testing::InitGoogleTest(&argc, argv);
        // launch the test
        return RUN_ALL_TESTS();
    }
```

gtest.h中提供了一些方便的宏。包括如上代码中的 TEST, EXPECT_EQ, RUN_ALL_TESTS等。 
TEST(TestName, TestCaseName){
}可以方便的定义一个TestCase，这个宏的作用是 定义一个新的 Test类，同时将这个类加入到一个由框架控制的测试容器中。
RUN_ALL_TESTS() 宏将已经加入到 测试容器中的东西逐个运行。
