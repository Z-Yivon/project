# Project17：比较Firefox和Chrome的记住密码插件的实现区别

##  Chrome记住密码实现

google保存的密码数据存储在位于此处的 SQLite 数据库中：

AppData\Local\Google\Chrome\User Data\ Local State

可以使用 SQLite 数据库浏览器打开此文件（文件名只是“登录数据”）并查看包含已保存密码的“登录”表。会注意到“password_value”字段不可读，因为该值已加密。


为了执行加密（在 Windows 上），Chrome 使用 Windows 提供的 API 函数，该函数使得加密数据只能由用于加密密码的 Windows 用户帐户解密。因此本质上，您的主密码就是您的 Windows 帐户密码。因此，一旦您使用帐户登录 Windows，Chrome 就可以解读此数据。

但是，由于您的 Windows 帐户密码是一个常量，因此对“主密码”的访问并非 Chrome 独有，因为外部实用程序也可以获取此数据并对其进行解密。使用 NirSoft 提供的免费实用程序 ChromePass，您可以查看所有保存的密码数据并轻松将其导出到纯文本文件。

因此，如果 ChromePass 实用程序可以访问这些数据，那么以相应用户身份运行的恶意软件也可以访问它，这是有道理的。当ChromePass.exe 上传到 VirusTotal时，超过一半的防病毒引擎将其标记为危险。虽然在这种情况下该实用程序是安全的，但令人有点放心的是，这种行为至少被许多 AV 软件包标记（尽管 Microsoft Security Essentials 不是报告其危险的 AV 引擎之一）

Google Chrome 为您提供了一个默认工具，无需安装即可保存您的登录凭据。它使用 AES 256 位 SSL/TLS 加密以及密码短语功能，为您的密码和个人信息提供额外的安全性。除了生成和保存密码之外，您还可以通过 Chrome 的密码检查查看您的登录信息。该功能默认启用。
## FireFox记住密码

Firefox 的同步是一个本地 AES-256-CBC 加密数据库，存储您的资料（可以包括密码），存储在 Mozilla 的服务器上。该密钥不会以未加密的形式离开您的浏览器，除了您之外，任何人都可以解密。但它最终会出现在您同步的每个 Firefox 浏览器上。

同步密钥存储在您本地的密码中。如果您没有 Firefox 主密码，则该密码不会在您的计算机上加密。如果您使用主密码，则从您将同步密钥输入 Firefox 的那一刻起，同步密钥就不会加密。

同步密钥可从您的浏览器获取。转到选项/Firefox 同步，单击“管理帐户”工具，选择“我的恢复密钥”，它将生成密钥的可打印版本。您可以在 Firefox 的任何其他实例中键入用户的电子邮件地址和该密钥，您将被纳入同步中，因此可以完全查看所有已同步的密码。

为满足开发者创建满足各种安全标准的应用程序，Mozilla开发了一个叫做“Network Security Services”,或叫NSS的开源库。Firefox使用其中一个叫做”Security Decoder Ring”，或叫SDR的API来帮助实现账号证书的加密和解密函数。firefox使用它完成加密:

当一个Firefox配置文件被首次创建时，一个叫做SDR的随机key和一个Salt(译者注：Salt，在密码学中，是指通过在密码任意固定位置插入特定的字符串，让散列后的结果和使用原始密码的散列结果不相符，这种过程称之为“加盐”)就会被创建并存储在一个名为“key3.db”的文件中。利用这个key和盐，使用3DES加密算法来加密用户名和密码。密文是Base64编码的，并存储在一个叫做signons.sqlite的sqlite数据库中。Signons.sqlite和key3.db文件均位于%APPDATA%\Mozilla\Firefox\Profiles\[random_profile]目录。

所以我们要做的就是得到SDR密钥。正如此处解释的，这个key被保存在一个叫PCKS#11软件“令牌”的容器中。该令牌被封装进入内部编号为PKCS#11的“槽位”中。因此需要访问该槽位来破译账户证书。

还有一个问题，这个SDR也是用3DES(DES-EDE-CBC)算法加密的。解密密钥是Mozilla叫做“主密码”的hash值，以及一个位于key3.db文件中对应的叫做“全局盐”的值。

Firefox用户可以在浏览器的设置中设定主密码，但关键是好多用户不知道这个特性。正如我们看到的，用户整个账号证书的完整性链条依赖于安全设置中选择的密码，它是攻击者唯一不知道的值。如果用户使用一个强健的主密码，那么攻击者想要恢复存储的证书是不太可能的。

那么——如果用户没有设置主密码，空密码就会被使用。这意味着攻击者可以提取全局盐，获得它与空密码做hash运算结果，然后使用该结果破译SDR密钥。再用破译的SDR密钥危害用户证书。


## 比较

Firefox 和 Chrome 都有本机密码管理器，允许用户安全地存储其各种在线帐户的密码。Firefox 的密码管理器使用主密码来“解锁”您保存的其余密码，而 Chrome 只保存每个密码。要求主密码可以防止其他人在碰巧有权访问您的设备或浏览器时登录您的帐户，从而使 Firefox 的密码管理器更加安全。

相比于chrome浏览器，firefox记住密码功能实现更复杂，安全性更高

## 参考：
[https://www.woshipm.com/pmd/35985.html](https://security.stackexchange.com/questions/41029/comparison-between-firefox-password-manager-and-chrome-password-manager)
