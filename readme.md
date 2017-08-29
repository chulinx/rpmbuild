#### 自己编写测试过的spec
- 打包工具安装
```bash
yum -y install rpm-build
```
- 使用方法：
```bash
cd ~
git clone https://github.com/chulinx/rpmbuild.git && cd rpmbuild/SPEC/ && rpmbuild -ba **.spec
```
- 关于原理和详细点的打包过程请参考我的博客的一篇博文
 **[rpm打包](https://chulinx.github.io/2017/08/11/RpmBuild%E6%89%93%E5%8C%85%E6%80%BB%E7%BB%93/#more)**
