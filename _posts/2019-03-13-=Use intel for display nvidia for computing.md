---
layout: post
title: Use intel for display nvidia for computing
description: 
category: 
tags: 
---
{% include JB/setup %}


# Problems:

For a iGPU and Nvidia GPU system with Ubuntu 17.04 Desktop, cuda 8.0.  

If use prime-select nvidia, then nvidia GPU are both used as display and computing.  

If use prime-select intel, then nvidia-smi and deviceQuery will not found the Nvidia GPU in system.
and propmts that libnvidia-ml.so can not be found.


# Way to solve:

<pre>
    sudo echo "/usr/lib/nvidia-375" >> /etc/ld.so.conf.d/nvidia.conf
</pre>
note that the path is which contains the libnvidia-ml.so file in your system.


# Ads and Cons of use Intel for display

Normally the CPU fan will have a little noise when in idle mode than GPU in idle mode, if you do not use your system for heavy
tasks. The good thing is you will have more GPU memory for you cuda computing with out the display thing consume you nvidia GPU mem. This is better if you want to use you nvidia GPU for some machine learning tasks, which are normally more memory consuming if you want to exersize on read world data.


## Follow up on Ubuntuu 18.04, nvidia-driver 410.78

When I installed new Ubuntu 18.04, and use the run files from nvidia driver website [https://tw.download.nvidia.com/XFree86/Linux-x86_64/410.78/NVIDIA-Linux-x86_64-410.78.run](https://tw.download.nvidia.com/XFree86/Linux-x86_64/410.78/NVIDIA-Linux-x86_64-410.78.run)
And run the install with   `NVIDIA-Linux-x86_64-410.48.run --no-opengl-files`, then nvidia driver will not install openGL libraries to my system. 
So the thoritically, my system only can use the intel iGPU for OpenGL, and it should use the iGPU for any hardware video/graphics acceleration. 
But it doesn't.

### Issues
To be more concret, I can observe serveal issues in my system.
1. `glmark2` and `glxinfo` shows the OpenGL driver is `Vmware` provided, just like what's been done in the virtual machine, which has basiacally very suck visual acceleration.
```
litao@deep: ~ $ glmark2                                                                                                                             
** GLX does not support GLX_EXT_swap_control or GLX_MESA_swap_control!
** Failed to set swap interval. Results may be bounded above by refresh rate.
=======================================================
    glmark2 2014.03+git20150611.fa71af2d
=======================================================
    OpenGL Information
    GL_VENDOR:     VMware, Inc.
    GL_RENDERER:   llvmpipe (LLVM 6.0, 256 bits)
    GL_VERSION:    3.0 Mesa 18.0.5
=======================================================
...
```

```
litao@deep: ~ $ glxinfo | grep OpenGL | grep string                                                                                                                                                 [1:13:48]
OpenGL vendor string: VMware, Inc.
OpenGL renderer string: llvmpipe (LLVM 6.0, 256 bits)
OpenGL core profile version string: 3.3 (Core Profile) Mesa 18.0.5
OpenGL core profile shading language version string: 3.30
OpenGL version string: 3.0 Mesa 18.0.5
OpenGL shading language version string: 1.30
OpenGL ES profile version string: OpenGL ES 3.0 Mesa 18.0.5
OpenGL ES profile shading language version string: OpenGL ES GLSL ES 3.00
```

2. intel_gpu_top shows very GPU activity when I use the chrome to play videos and use any video players
`sudo intel_gpu_top`
<img src ="/assets/pic/intel_gpu_top.low.png" align="center" alt="intel_gpu_top" style="max-width:100%;" />

3. Gnome graphics animation sucks, almost every thing is very slow.

4. nvidia-smi shows there are x-server process running on nvidia gpu, which consumes when precious GPU memory when I want to use them as pure cuda compute device in linux. The out are like the following.
```
Sat Mar 16 01:12:53 2019       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 410.78       Driver Version: 410.78       CUDA Version: 10.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX 106...  Off  | 00000000:01:00.0  On |                  N/A |
| 29%   31C    P8     9W / 120W |    164MiB /  6078MiB |      2%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0     13305      G   /usr/lib/xorg/Xorg                            32MiB |
|    0     13700      G   /usr/lib/xorg/Xorg                           129MiB |
+-----------------------------------------------------------------------------+
```


### Solution

There should be serveral solutions, and they should have the same functionality, while everyone can choose any one of this by their own need.

#### Blacklist nvidia-drm module 
 The first solution is what I have achived based on my system, and I don't need to re-install the nvidia-driver.
Only add the following to `/etc/modprobe.d/blacklist-nvidia.conf`
```
blacklist nvidia-drm
alias nvidia-drm off
```
Then optionally (I don't know why it's needed or not, but both works) run the command `update-initramfs`, to re-genetate the initramfs.

I guess this would disable the `nvidia-drm` module, which used for the X-display related things, but not leave the other nvidia driver module to be enabled. Because, in last section, we can see that `prime-select intel` commnad also generate a black list to disable all `nvidia` and `nvidia-drm` and `nvidia-modset` module.  To make the cuda program run, we need to keep the `nvidia` and `nvidia-modset` by commenting them out of the blacklist.

``` 
#blacklist nvidia
blacklist nvidia-drm
#blacklist nvidia-modeset
#alias nvidia off
alias nvidia-drm off
#alias nvidia-modeset off
```
#### Use --no-drm option when install nvidia driver from a runfile.

I didn't test it, but it should works like a charm, since blacklist the module works. 
The option explanation can be found by `nvidia-installer -A` commmand if you already had nvidia driver installed.
```
litao@deep: ~ $ nvidia-installer -A  | grep drm                       [1:21:06]
  --no-drm
      Do not install the nvidia-drm kernel module. This kernel module provides
      that run independently of X11. The '--no-drm' option should only be used
      to work around failures to build or install the nvidia-drm kernel module
```

#### Install the nvidia-headless-XXX driver package provided by apt

I didn't test it, but it should work, the following is that the package said by apt show. And it should have the same functionality as 
--no-drm option when you use the runfile. Please google it before you try this method.
```
litao@deep: ~ $ apt show nvidia-headless-390                                                                                         [1:21:11]
Package: nvidia-headless-390
#.....ignore serveral un-useful lines.
Description: NVIDIA headless metapackage
 This metapackage installs the NVIDIA driver and the libraries that enable
 parallel general purpose computation through CUDA and
 OpenCL.
 .
 Install this package if you do not need X11 or Wayland support, which is
 provided by the nvidia-driver-390 metapackage.
```

#### Tips need to be considerd when install cuda

After you installed the nvidia-driver, you may also want to install a cuda toolkit used to develop cuda programm.

And when you do that, sometimes cuda installation tool will overwrite your driver install with the one attached with cuda installer.
Please pay attention on that. This may overwrite. what you have already done 
I suggest to install cuda toolkit by running file, and the install guide can be found here.
https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#runfile-advanced

I use this command, 
`sudo cuda-linux.10.0.130-24817639.run --toolkit --samples	--no-opengl-libs`


### How to test if I have successfully solve the problem?

1. glmark2 and glxinfo are showing right info about intel OpenGL like the following
```bash
litao@deep: ~ $ glmark2                                                                                                                                                                            [23:55:17]
=======================================================
    glmark2 2014.03+git20150611.fa71af2d
=======================================================
    OpenGL Information
    GL_VENDOR:     Intel Open Source Technology Center
    GL_RENDERER:   Mesa DRI Intel(R) HD Graphics 630 (Kaby Lake GT2) 
    GL_VERSION:    3.0 Mesa 18.0.5
=======================================================
```
```bash
litao@deep: ~ $ glxinfo | grep OpenGL | grep string                                                                                                          [0:11:11]
OpenGL vendor string: Intel Open Source Technology Center
OpenGL renderer string: Mesa DRI Intel(R) HD Graphics 630 (Kaby Lake GT2) 
OpenGL core profile version string: 4.5 (Core Profile) Mesa 18.0.5
OpenGL core profile shading language version string: 4.50
OpenGL version string: 3.0 Mesa 18.0.5
OpenGL shading language version string: 1.30
OpenGL ES profile version string: OpenGL ES 3.2 Mesa 18.0.5
OpenGL ES profile shading language version string: OpenGL ES GLSL ES 3.20
```

2. `nvidia-smi` shows no xserver process and 'no running process' when you don't run any cuda program.

litao@deep: ~ $ nvidia-smi                                                                                                                                                                         [23:56:38]
Fri Mar 15 23:56:50 2019       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 410.78       Driver Version: 410.78       CUDA Version: 10.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX 106...  Off  | 00000000:01:00.0 Off |                  N/A |
| 37%   31C    P0    26W / 120W |      0MiB /  6078MiB |      3%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+

3. intel_gpu_top shows the following when you playing an chrome youtube `video`, it should using intel open gl to do haraware accelerate.
`sudo intel_gpu_top`
<img src ="/assets/pic/intel_gpu_top.ok.png" align="center" alt="intel_gpu_top" style="max-width:100%;" />

4. lsmod to show loaded nvidia and intel mod driver.

```bash
litao@deep: ~ $ lsmod | grep intel                                                                                                                           [0:26:23]
intel_rapl             20480  0
intel_powerclamp       16384  0
kvm_intel             212992  0
kvm                   598016  1 kvm_intel
ghash_clmulni_intel    16384  0
aesni_intel           188416  3
aes_x86_64             20480  1 aesni_intel
crypto_simd            16384  1 aesni_intel
glue_helper            16384  1 aesni_intel
cryptd                 24576  3 crypto_simd,ghash_clmulni_intel,aesni_intel
snd_hda_intel          40960  8
intel_cstate           20480  0
intel_rapl_perf        16384  0
snd_hda_codec         126976  4 snd_hda_codec_generic,snd_hda_codec_hdmi,snd_hda_intel,snd_hda_codec_realtek
snd_hda_core           81920  5 snd_hda_codec_generic,snd_hda_codec_hdmi,snd_hda_intel,snd_hda_codec,snd_hda_codec_realtek
snd_pcm                98304  4 snd_hda_codec_hdmi,snd_hda_intel,snd_hda_codec,snd_hda_core
btintel                16384  1 btusb
bluetooth             548864  33 btrtl,btintel,btbcm,bnep,btusb,rfcomm
snd                    81920  27 snd_hda_codec_generic,snd_seq,snd_seq_device,snd_hda_codec_hdmi,snd_hwdep,snd_hda_intel,snd_hda_codec,snd_hda_codec_realtek,snd_timer,snd_pcm,snd_rawmidi
```

Only `nvidia` was loaded, not any `nvidia-drm` thing.
```
itao@deep: ~ $ lsmod | grep nvidia                                                                                                                          [0:26:51]
nvidia              16588800  0
ipmi_msghandler        53248  2 ipmi_devintf,nvidia
```

### Things does work, or work but in the wrong way.

1. `prime-select` command provided by `nvidia-prime` package.
When use `sudo prime-select intel` do switch to the iGPU only, and disabls the nvidia gpu. 
I can observe that openGL part is correct, and I can use intel iGPU to accelerate chrome/video stuff. 
But when I run `nvidia-smi`, it gives an error like the following， and it errors by "can not find any cuda devices", when I run `deviceQuery` sample or any cuda program.

```
litao@deep: ~ $ nvidia-smi                                                                                                                          
NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver. Make sure that the latest NVIDIA driver is installed and running.

FAIL: 9
```

```
./deviceQuery Starting...

 CUDA Device Query (Runtime API) version (CUDART static linking)

cudaGetDeviceCount returned 38
-> no CUDA-capable device is detected
Result = FAIL
FAIL: 1
```
I tried to follow tthe first section which I found useful in old ubuntu (although I don't remember why and how.)
To add `/usr/lib/x86_64-linux-gpu` (where the libnvidia-ml.so was, found by locate libnvidia-ml.so), to /etc/ld.so.conf.d/nvidia.conf , and 
re-run the `sudo ldconfig`. I still got the same error when runing `nvidia-smi`.


The reason why `prime-select intel` works for OpenGL, and make the nvidia gpu totally lost, is because it just completely disbaled any `nvidia` driver (includeing nouveau and nvidia private driver).

* The command will write the following content to  `/etc/modprobe.d/blacklist-nvidia.conf` file, 
``` 
blacklist nvidia
blacklist nvidia-drm
blacklist nvidia-modeset
alias nvidia off
alias nvidia-drm off
alias nvidia-modeset off
```
then the commnad will re-generate the initfs by `update-initramfs`.

* Addtionally, the command will add the kernel starting command line parameters `nouveau.runpm=0` to `/boot/grub/grub.cfg`, like the following 
```
<linux	/boot/vmlinuz-4.15.0-46-generic root=UUID=785c9aa3-fff4-4c78-b4b8-390619ea4184 ro  quiet splash $vt_handoff
===
>linux	/boot/vmlinuz-4.15.0-46-generic root=UUID=785c9aa3-fff4-4c78-b4b8-390619ea4184 ro  quiet splash nouveau.runpm=0 $vt_handoff
```
About the meaning, please google it, basically it means to disable the 'nouveau' driver(open source version of nvidia gpu driver). 

* Addtionally, the `prime-select intel` command will install a service to the system, which basically do the following during some phase in the startup stage (I don't remember whem, but that's what it does.). About the meaning of this, please see [Ubuntu HybridGraphics](https://help.ubuntu.com/community/HybridGraphics)
```
 echo OFF > /sys/kernel/debug/vgaswitcheroo/switch
```

### About the /etc/X11/xorg.conf

If you install nvidia driver, and not blacked (suppose you didn't exclude them during any install method), you will need nvidia device defined in the xorg.conf. Then you could properly use the display connect to nvidia gpu. Here is the mine.

```
Section "ServerLayout"
    Identifier     "Layout0"
    Screen      0  "Screen0"
    Screen      1  "Screen1"
    InputDevice    "Keyboard0" "CoreKeyboard"
    InputDevice    "Mouse0" "CorePointer"
EndSection

Section "Files"
EndSection

Section "InputDevice"
    # generated from default
    Identifier     "Mouse0"
    Driver         "mouse"
    Option         "Protocol" "auto"
    Option         "Device" "/dev/psaux"
    Option         "Emulate3Buttons" "no"
    Option         "ZAxisMapping" "4 5"
EndSection

Section "InputDevice"
    # generated from default
    Identifier     "Keyboard0"
    Driver         "kbd"
EndSection

Section "Monitor"
    Identifier     "Monitor0"
    VendorName     "Unknown"
    ModelName      "Unknown"
    HorizSync       28.0 - 33.0
    VertRefresh     43.0 - 72.0
    Option         "DPMS"
EndSection

Section "Device"
    Identifier     "Device0"
    Driver         "intel"
    VendorName     "Intel"
EndSection

Section "Screen"
    Identifier     "Screen0"
    Device         "Device0"
    Monitor        "Monitor0"
    DefaultDepth    24
    SubSection     "Display"
        Depth       24
    EndSubSection
EndSection

Section "Device"
    Identifier     "Device1"
    Driver         "nvidia"
    VendorName     "NVIDIA Corporation"
EndSection

Section "Screen"
    Identifier     "Screen1"
    Device         "Device1"
    Monitor        "Monitor0"
    DefaultDepth    24
    SubSection     "Display"
        Depth       24
    EndSubSection
EndSection
```

If you have blacklisted the nvidia-drm module, or just didn't install it. Your xorg.conf should not (alghou, it should work even you have nvidia device on the file?) contain nvidia dvice, and consider it as an intel only. My works are like following.

```
Section "ServerLayout"
    Identifier     "Layout0"
    Screen         "Screen0"
    InputDevice    "Keyboard0" "CoreKeyboard"
    InputDevice    "Mouse0" "CorePointer"
EndSection

Section "Files"
EndSection

Section "InputDevice"
    # generated from default
    Identifier     "Mouse0"
    Driver         "mouse"
    Option         "Protocol" "auto"
    Option         "Device" "/dev/psaux"
    Option         "Emulate3Buttons" "no"
    Option         "ZAxisMapping" "4 5"
EndSection

Section "InputDevice"
    # generated from default
    Identifier     "Keyboard0"
    Driver         "kbd"
EndSection

Section "Device"
    Identifier     "Device0"
    Driver         "intel"
    VendorName     "Intel"
EndSection

Section "Screen"
    Identifier     "Screen0"
    Device         "Device0"
EndSection
```


# Ref:
>[Nvidia-smi problem solved](https://standbymesss.blogspot.jp/2016/09/ubuntu-nvidia-smi-couldnt-find.html)
