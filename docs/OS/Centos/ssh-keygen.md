# ssh-keygen创建公钥私钥对

[[toc]]

## 1. 什么是SSH

SSH 为 Secure Shell的缩写，由 IETF 的网络小组（Network Working Group）所制定；它是建立在应用层基础上的安全协议。 

SSH 是目前较可靠，专为远程登录会话和其他网络服务提供安全性的协议。利用 SSH 协议可以有效防止远程管理过程中的信息泄露问题。 

SSH最初是UNIX系统上的一个程序，后来又迅速扩展到其他操作平台。

为了在不同平台/网络主机之间的通信安全, 很多时候我们都要通过ssh进行认证。 ssh认证方式主要有2种:

- 基于口令的安全认证: 每次登录的时候都要输入用户名和密码, 由于要在网络上传输密码, 可能存在中间人攻击的风险。
- 基于密钥的安全认证: 配置完成后就可以实现免密登录, 这种方式更加安全 —— 不需要在网络上传递口令, 只需要传输一次公钥。 常见的git的ssh方式就是通过公钥进行认证的。

测试使用的系统：

```sh
[root@ansible ~]# cat /etc/centos-release
CentOS Linux release 7.9.2009 (Core)
[root@ansible ~]#
```



我们使用`man`导出`ssh-keygen`的帮助手册信息:

```
SSH-KEYGEN(1)                                                                                                                 BSD General Commands Manual                                                                                                                SSH-KEYGEN(1)

NAME
     ssh-keygen — authentication key generation, management and conversion

SYNOPSIS
     ssh-keygen [-q] [-b bits] [-t dsa | ecdsa | ed25519 | rsa | rsa1] [-N new_passphrase] [-C comment] [-f output_keyfile]
     ssh-keygen -p [-P old_passphrase] [-N new_passphrase] [-f keyfile]
     ssh-keygen -i [-m key_format] [-f input_keyfile]
     ssh-keygen -e [-m key_format] [-f input_keyfile]
     ssh-keygen -y [-f input_keyfile]
     ssh-keygen -c [-P passphrase] [-C comment] [-f keyfile]
     ssh-keygen -l [-v] [-E fingerprint_hash] [-f input_keyfile]
     ssh-keygen -B [-f input_keyfile]
     ssh-keygen -D pkcs11
     ssh-keygen -F hostname [-f known_hosts_file] [-l]
     ssh-keygen -H [-f known_hosts_file]
     ssh-keygen -R hostname [-f known_hosts_file]
     ssh-keygen -r hostname [-f input_keyfile] [-g]
     ssh-keygen -G output_file [-v] [-b bits] [-M memory] [-S start_point]
     ssh-keygen -T output_file -f input_file [-v] [-a rounds] [-J num_lines] [-j start_line] [-K checkpt] [-W generator]
     ssh-keygen -s ca_key -I certificate_identity [-h] [-n principals] [-O option] [-V validity_interval] [-z serial_number] file ...
     ssh-keygen -L [-f input_keyfile]
     ssh-keygen -A
     ssh-keygen -k -f krl_file [-u] [-s ca_public] [-z version_number] file ...
     ssh-keygen -Q -f krl_file file ...

DESCRIPTION
     ssh-keygen generates, manages and converts authentication keys for ssh(1).  ssh-keygen can create keys for use by SSH protocol versions 1 and 2.  Protocol 1 should not be used and is only offered to support legacy devices.  It suffers from a number of cryptographic weak‐
     nesses and doesn't support many of the advanced features available for protocol 2.

     The type of key to be generated is specified with the -t option.  If invoked without any arguments, ssh-keygen will generate an RSA key for use in SSH protocol 2 connections.

     ssh-keygen is also used to generate groups for use in Diffie-Hellman group exchange (DH-GEX).  See the MODULI GENERATION section for details.

     Finally, ssh-keygen can be used to generate and update Key Revocation Lists, and to test whether given keys have been revoked by one.  See the KEY REVOCATION LISTS section for details.

     Normally each user wishing to use SSH with public key authentication runs this once to create the authentication key in ~/.ssh/identity, ~/.ssh/id_dsa, ~/.ssh/id_ecdsa, ~/.ssh/id_ed25519 or ~/.ssh/id_rsa.  Additionally, the system administrator may use this to generate
     host keys, as seen in /etc/rc.

     Normally this program generates the key and asks for a file in which to store the private key.  The public key is stored in a file with the same name but “.pub” appended.  The program also asks for a passphrase.  The passphrase may be empty to indicate no passphrase (host
     keys must have an empty passphrase), or it may be a string of arbitrary length.  A passphrase is similar to a password, except it can be a phrase with a series of words, punctuation, numbers, whitespace, or any string of characters you want.  Good passphrases are 10-30
     characters long, are not simple sentences or otherwise easily guessable (English prose has only 1-2 bits of entropy per character, and provides very bad passphrases), and contain a mix of upper and lowercase letters, numbers, and non-alphanumeric characters.  The
     passphrase can be changed later by using the -p option.

     There is no way to recover a lost passphrase.  If the passphrase is lost or forgotten, a new key must be generated and the corresponding public key copied to other machines.

     For RSA1 keys and keys stored in the newer OpenSSH format, there is also a comment field in the key file that is only for convenience to the user to help identify the key.  The comment can tell what the key is for, or whatever is useful.  The comment is initialized to
     “user@host” when the key is created, but can be changed using the -c option.

     After a key is generated, instructions below detail where the keys should be placed to be activated.

     The options are as follows:

     -A      For each of the key types (rsa1, rsa, dsa, ecdsa and ed25519) for which host keys do not exist, generate the host keys with the default key file path, an empty passphrase, default bits for the key type, and default comment.  This is used by /etc/rc to generate new
             host keys.

     -a rounds
             When saving a new-format private key (i.e. an ed25519 key or any SSH protocol 2 key when the -o flag is set), this option specifies the number of KDF (key derivation function) rounds used.  Higher numbers result in slower passphrase verification and increased
             resistance to brute-force password cracking (should the keys be stolen).

             When screening DH-GEX candidates ( using the -T command).  This option specifies the number of primality tests to perform.

     -B      Show the bubblebabble digest of specified private or public key file.

     -b bits
             Specifies the number of bits in the key to create.  For RSA keys, the minimum size is 1024 bits and the default is 2048 bits.  Generally, 2048 bits is considered sufficient.  DSA keys must be exactly 1024 bits as specified by FIPS 186-2.  For ECDSA keys, the -b
             flag determines the key length by selecting from one of three elliptic curve sizes: 256, 384 or 521 bits.  Attempting to use bit lengths other than these three values for ECDSA keys will fail.  Ed25519 keys have a fixed length and the -b flag will be ignored.

     -C comment
             Provides a new comment.

     -c      Requests changing the comment in the private and public key files.  This operation is only supported for RSA1 keys and keys stored in the newer OpenSSH format.  The program will prompt for the file containing the private keys, for the passphrase if the key has one,
             and for the new comment.

     -D pkcs11
             Download the RSA public keys provided by the PKCS#11 shared library pkcs11.  When used in combination with -s, this option indicates that a CA key resides in a PKCS#11 token (see the CERTIFICATES section for details).

     -E fingerprint_hash
             Specifies the hash algorithm used when displaying key fingerprints.  Valid options are: “md5” and “sha256”.  The default is “sha256”.

     -e      This option will read a private or public OpenSSH key file and print to stdout the key in one of the formats specified by the -m option.  The default export format is “RFC4716”.  This option allows exporting OpenSSH keys for use by other programs, including several
             commercial SSH implementations.

     -F hostname
             Search for the specified hostname in a known_hosts file, listing any occurrences found.  This option is useful to find hashed host names or addresses and may also be used in conjunction with the -H option to print found keys in a hashed format.

     -f filename
             Specifies the filename of the key file.

     -G output_file
             Generate candidate primes for DH-GEX.  These primes must be screened for safety (using the -T option) before use.

     -g      Use generic DNS format when printing fingerprint resource records using the -r command.

     -H      Hash a known_hosts file.  This replaces all hostnames and addresses with hashed representations within the specified file; the original content is moved to a file with a .old suffix.  These hashes may be used normally by ssh and sshd, but they do not reveal identi‐
             fying information should the file's contents be disclosed.  This option will not modify existing hashed hostnames and is therefore safe to use on files that mix hashed and non-hashed names.

     -h      When signing a key, create a host certificate instead of a user certificate.  Please see the CERTIFICATES section for details.

     -I certificate_identity
             Specify the key identity when signing a public key.  Please see the CERTIFICATES section for details.

     -i      This option will read an unencrypted private (or public) key file in the format specified by the -m option and print an OpenSSH compatible private (or public) key to stdout.  This option allows importing keys from other software, including several commercial SSH
             implementations.  The default import format is “RFC4716”.

     -J num_lines
             Exit after screening the specified number of lines while performing DH candidate screening using the -T option.

     -j start_line
             Start screening at the specified line number while performing DH candidate screening using the -T option.

     -K checkpt
             Write the last line processed to the file checkpt while performing DH candidate screening using the -T option.  This will be used to skip lines in the input file that have already been processed if the job is restarted.

     -k      Generate a KRL file.  In this mode, ssh-keygen will generate a KRL file at the location specified via the -f flag that revokes every key or certificate presented on the command line.  Keys/certificates to be revoked may be specified by public key file or using the
             format described in the KEY REVOCATION LISTS section.

     -L      Prints the contents of one or more certificates.

     -l      Show fingerprint of specified public key file.  Private RSA1 keys are also supported.  For RSA and DSA keys ssh-keygen tries to find the matching public key file and prints its fingerprint.  If combined with -v, a visual ASCII art representation of the key is sup‐
             plied with the fingerprint.

     -M memory
             Specify the amount of memory to use (in megabytes) when generating candidate moduli for DH-GEX.

     -m key_format
             Specify a key format for the -i (import) or -e (export) conversion options.  The supported key formats are: “RFC4716” (RFC 4716/SSH2 public or private key), “PKCS8” (PEM PKCS8 public key) or “PEM” (PEM public key).  The default conversion format is “RFC4716”.

     -N new_passphrase
             Provides the new passphrase.

     -n principals
             Specify one or more principals (user or host names) to be included in a certificate when signing a key.  Multiple principals may be specified, separated by commas.  Please see the CERTIFICATES section for details.

     -O option
             Specify a certificate option when signing a key.  This option may be specified multiple times.  Please see the CERTIFICATES section for details.  The options that are valid for user certificates are:

             clear   Clear all enabled permissions.  This is useful for clearing the default set of permissions so permissions may be added individually.

             force-command=command
                     Forces the execution of command instead of any shell or command specified by the user when the certificate is used for authentication.

             no-agent-forwarding
                     Disable ssh-agent(1) forwarding (permitted by default).

             no-port-forwarding
                     Disable port forwarding (permitted by default).

             no-pty  Disable PTY allocation (permitted by default).

             no-user-rc
                     Disable execution of ~/.ssh/rc by sshd(8) (permitted by default).

             no-x11-forwarding
                     Disable X11 forwarding (permitted by default).

             permit-agent-forwarding
                     Allows ssh-agent(1) forwarding.

             permit-port-forwarding
                     Allows port forwarding.

             permit-pty
                     Allows PTY allocation.

             permit-user-rc
                     Allows execution of ~/.ssh/rc by sshd(8).

             permit-x11-forwarding
                     Allows X11 forwarding.

             source-address=address_list
                     Restrict the source addresses from which the certificate is considered valid.  The address_list is a comma-separated list of one or more address/netmask pairs in CIDR format.

             At present, no options are valid for host keys.

     -o      Causes ssh-keygen to save private keys using the new OpenSSH format rather than the more compatible PEM format.  The new format has increased resistance to brute-force password cracking but is not supported by versions of OpenSSH prior to 6.5.  Ed25519 keys always
             use the new private key format.

     -P passphrase
             Provides the (old) passphrase.

     -p      Requests changing the passphrase of a private key file instead of creating a new private key.  The program will prompt for the file containing the private key, for the old passphrase, and twice for the new passphrase.

     -Q      Test whether keys have been revoked in a KRL.

     -q      Silence ssh-keygen.

     -R hostname
             Removes all keys belonging to hostname from a known_hosts file.  This option is useful to delete hashed hosts (see the -H option above).

     -r hostname
             Print the SSHFP fingerprint resource record named hostname for the specified public key file.

     -S start
             Specify start point (in hex) when generating candidate moduli for DH-GEX.

     -s ca_key
             Certify (sign) a public key using the specified CA key.  Please see the CERTIFICATES section for details.

             When generating a KRL, -s specifies a path to a CA public key file used to revoke certificates directly by key ID or serial number.  See the KEY REVOCATION LISTS section for details.

     -T output_file
             Test DH group exchange candidate primes (generated using the -G option) for safety.

     -t dsa | ecdsa | ed25519 | rsa | rsa1
             Specifies the type of key to create.  The possible values are “rsa1” for protocol version 1 and “dsa”, “ecdsa”, “ed25519”, or “rsa” for protocol version 2.

     -u      Update a KRL.  When specified with -k, keys listed via the command line are added to the existing KRL rather than a new KRL being created.

     -V validity_interval
             Specify a validity interval when signing a certificate.  A validity interval may consist of a single time, indicating that the certificate is valid beginning now and expiring at that time, or may consist of two times separated by a colon to indicate an explicit
             time interval.  The start time may be specified as a date in YYYYMMDD format, a time in YYYYMMDDHHMMSS format or a relative time (to the current time) consisting of a minus sign followed by a relative time in the format described in the TIME FORMATS section of
             sshd_config(5).  The end time may be specified as a YYYYMMDD date, a YYYYMMDDHHMMSS time or a relative time starting with a plus character.

             For example: “+52w1d” (valid from now to 52 weeks and one day from now), “-4w:+4w” (valid from four weeks ago to four weeks from now), “20100101123000:20110101123000” (valid from 12:30 PM, January 1st, 2010 to 12:30 PM, January 1st, 2011), “-1d:20110101” (valid
             from yesterday to midnight, January 1st, 2011).

     -v      Verbose mode.  Causes ssh-keygen to print debugging messages about its progress.  This is helpful for debugging moduli generation.  Multiple -v options increase the verbosity.  The maximum is 3.

     -W generator
             Specify desired generator when testing candidate moduli for DH-GEX.

     -y      This option will read a private OpenSSH format file and print an OpenSSH public key to stdout.

     -z serial_number
             Specifies a serial number to be embedded in the certificate to distinguish this certificate from others from the same CA.  The default serial number is zero.

             When generating a KRL, the -z flag is used to specify a KRL version number.

MODULI GENERATION
     ssh-keygen may be used to generate groups for the Diffie-Hellman Group Exchange (DH-GEX) protocol.  Generating these groups is a two-step process: first, candidate primes are generated using a fast, but memory intensive process.  These candidate primes are then tested for
     suitability (a CPU-intensive process).

     Generation of primes is performed using the -G option.  The desired length of the primes may be specified by the -b option.  For example:

           # ssh-keygen -G moduli-2048.candidates -b 2048

     By default, the search for primes begins at a random point in the desired length range.  This may be overridden using the -S option, which specifies a different start point (in hex).

     Once a set of candidates have been generated, they must be screened for suitability.  This may be performed using the -T option.  In this mode ssh-keygen will read candidates from standard input (or a file specified using the -f option).  For example:

           # ssh-keygen -T moduli-2048 -f moduli-2048.candidates

     By default, each candidate will be subjected to 100 primality tests.  This may be overridden using the -a option.  The DH generator value will be chosen automatically for the prime under consideration.  If a specific generator is desired, it may be requested using the -W
     option.  Valid generator values are 2, 3, and 5.

     Screened DH groups may be installed in /etc/ssh/moduli.  It is important that this file contains moduli of a range of bit lengths and that both ends of a connection share common moduli.

CERTIFICATES
     ssh-keygen supports signing of keys to produce certificates that may be used for user or host authentication.  Certificates consist of a public key, some identity information, zero or more principal (user or host) names and a set of options that are signed by a Certifica‐
     tion Authority (CA) key.  Clients or servers may then trust only the CA key and verify its signature on a certificate rather than trusting many user/host keys.  Note that OpenSSH certificates are a different, and much simpler, format to the X.509 certificates used in
     ssl(8).

     ssh-keygen supports two types of certificates: user and host.  User certificates authenticate users to servers, whereas host certificates authenticate server hosts to users.  To generate a user certificate:

           $ ssh-keygen -s /path/to/ca_key -I key_id /path/to/user_key.pub

     The resultant certificate will be placed in /path/to/user_key-cert.pub.  A host certificate requires the -h option:

           $ ssh-keygen -s /path/to/ca_key -I key_id -h /path/to/host_key.pub

     The host certificate will be output to /path/to/host_key-cert.pub.

     It is possible to sign using a CA key stored in a PKCS#11 token by providing the token library using -D and identifying the CA key by providing its public half as an argument to -s:

           $ ssh-keygen -s ca_key.pub -D libpkcs11.so -I key_id user_key.pub

     In all cases, key_id is a "key identifier" that is logged by the server when the certificate is used for authentication.

     Certificates may be limited to be valid for a set of principal (user/host) names.  By default, generated certificates are valid for all users or hosts.  To generate a certificate for a specified set of principals:

           $ ssh-keygen -s ca_key -I key_id -n user1,user2 user_key.pub
           $ ssh-keygen -s ca_key -I key_id -h -n host.domain host_key.pub

     Additional limitations on the validity and use of user certificates may be specified through certificate options.  A certificate option may disable features of the SSH session, may be valid only when presented from particular source addresses or may force the use of a spe‐
     cific command.  For a list of valid certificate options, see the documentation for the -O option above.

     Finally, certificates may be defined with a validity lifetime.  The -V option allows specification of certificate start and end times.  A certificate that is presented at a time outside this range will not be considered valid.  By default, certificates are valid from UNIX
     Epoch to the distant future.

     For certificates to be used for user or host authentication, the CA public key must be trusted by sshd(8) or ssh(1).  Please refer to those manual pages for details.

KEY REVOCATION LISTS
     ssh-keygen is able to manage OpenSSH format Key Revocation Lists (KRLs).  These binary files specify keys or certificates to be revoked using a compact format, taking as little as one bit per certificate if they are being revoked by serial number.

     KRLs may be generated using the -k flag.  This option reads one or more files from the command line and generates a new KRL.  The files may either contain a KRL specification (see below) or public keys, listed one per line.  Plain public keys are revoked by listing their
     hash or contents in the KRL and certificates revoked by serial number or key ID (if the serial is zero or not available).

     Revoking keys using a KRL specification offers explicit control over the types of record used to revoke keys and may be used to directly revoke certificates by serial number or key ID without having the complete original certificate on hand.  A KRL specification consists
     of lines containing one of the following directives followed by a colon and some directive-specific information.

     serial: serial_number[-serial_number]
             Revokes a certificate with the specified serial number.  Serial numbers are 64-bit values, not including zero and may be expressed in decimal, hex or octal.  If two serial numbers are specified separated by a hyphen, then the range of serial numbers including and
             between each is revoked.  The CA key must have been specified on the ssh-keygen command line using the -s option.

     id: key_id
             Revokes a certificate with the specified key ID string.  The CA key must have been specified on the ssh-keygen command line using the -s option.

     key: public_key
             Revokes the specified key.  If a certificate is listed, then it is revoked as a plain public key.

     sha1: public_key
             Revokes the specified key by its SHA1 hash.

     KRLs may be updated using the -u flag in addition to -k.  When this option is specified, keys listed via the command line are merged into the KRL, adding to those already there.

     It is also possible, given a KRL, to test whether it revokes a particular key (or keys).  The -Q flag will query an existing KRL, testing each key specified on the command line.  If any key listed on the command line has been revoked (or an error encountered) then
     ssh-keygen will exit with a non-zero exit status.  A zero exit status will only be returned if no key was revoked.

FILES
     ~/.ssh/identity
             Contains the protocol version 1 RSA authentication identity of the user.  This file should not be readable by anyone but the user.  It is possible to specify a passphrase when generating the key; that passphrase will be used to encrypt the private part of this file
             using 3DES.  This file is not automatically accessed by ssh-keygen but it is offered as the default file for the private key.  ssh(1) will read this file when a login attempt is made.

     ~/.ssh/identity.pub
             Contains the protocol version 1 RSA public key for authentication.  The contents of this file should be added to ~/.ssh/authorized_keys on all machines where the user wishes to log in using RSA authentication.  There is no need to keep the contents of this file
             secret.

     ~/.ssh/id_dsa
     ~/.ssh/id_ecdsa
     ~/.ssh/id_ed25519
     ~/.ssh/id_rsa
             Contains the protocol version 2 DSA, ECDSA, Ed25519 or RSA authentication identity of the user.  This file should not be readable by anyone but the user.  It is possible to specify a passphrase when generating the key; that passphrase will be used to encrypt the
             private part of this file using 128-bit AES.  This file is not automatically accessed by ssh-keygen but it is offered as the default file for the private key.  ssh(1) will read this file when a login attempt is made.

     ~/.ssh/id_dsa.pub
     ~/.ssh/id_ecdsa.pub
     ~/.ssh/id_ed25519.pub
     ~/.ssh/id_rsa.pub
             Contains the protocol version 2 DSA, ECDSA, Ed25519 or RSA public key for authentication.  The contents of this file should be added to ~/.ssh/authorized_keys on all machines where the user wishes to log in using public key authentication.  There is no need to keep
             the contents of this file secret.

     /etc/ssh/moduli
             Contains Diffie-Hellman groups used for DH-GEX.  The file format is described in moduli(5).

ENVIRONMENT
     SSH_USE_STRONG_RNG
             The reseeding of the OpenSSL random generator is usually done from /dev/urandom.  If the SSH_USE_STRONG_RNG environment variable is set to value other than 0 the OpenSSL random generator is reseeded from /dev/random.  The number of bytes read is defined by the
             SSH_USE_STRONG_RNG value.  Minimum is 14 bytes.  This setting is not recommended on the computers without the hardware random generator because insufficient entropy causes the connection to be blocked until enough entropy is available.

SEE ALSO
     ssh(1), ssh-add(1), ssh-agent(1), moduli(5), sshd(8)

     The Secure Shell (SSH) Public Key File Format, RFC 4716, 2006.

AUTHORS
     OpenSSH is a derivative of the original and free ssh 1.2.12 release by Tatu Ylonen.  Aaron Campbell, Bob Beck, Markus Friedl, Niels Provos, Theo de Raadt and Dug Song removed many bugs, re-added newer features and created OpenSSH.  Markus Friedl contributed the support for
     SSH protocol versions 1.5 and 2.0.

BSD                                                                                                                                January 10, 2024                                                                                                                                BSD
```



## 2. 生成密钥对

为了不影响`root`账号的密钥信息，我新建一个`reader`账号，并在该账号下操作。

```sh
# 创建reader账号
[root@ansible ~]# useradd reader

# 切换到`reader`账号下
[root@ansible ~]# su - reader
Last login: Wed Jan 10 20:41:20 CST 2024 on pts/0
[reader@ansible ~]$
```



### 2.1 默认方式生成密钥对

直接输入`ssh-keygen`回车即可。

```sh
[reader@ansible ~]$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/reader/.ssh/id_rsa):
Created directory '/home/reader/.ssh'.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/reader/.ssh/id_rsa.
Your public key has been saved in /home/reader/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:IZZxAMiKdj+z4QvGxOQfWfkN5xwf/r4vjzFAPTgJTdQ reader@ansible
The key's randomart image is:
+---[RSA 2048]----+
| . ...o.. .+o.   |
|  o    +.  ..+E  |
|.. .  +o.. o=.o  |
|o.+. .o...*.+... |
|. .+.o  S. +.o   |
|  o .=.      ..  |
|   +..=       o. |
|  . .o        o+ |
|     ..       .==|
+----[SHA256]-----+
[reader@ansible ~]$
```

以上是我按默认方式生成密钥对的过程，以下增加以下说明：

```sh
# 按默认方式生成密钥对
[reader@ansible ~]$ ssh-keygen
# <--- 此处说明会产生RSA密钥对，可以通过 -t dsa | ecdsa | ed25519 | rsa | rsa1 参数来指定生成密钥加密算法
Generating public/private rsa key pair.   
# <--- 指定文件路径，默认存放在家目录的.ssh目录，你可以指定别的目录
# <--- 也可以通过-f filename 参数来指定文件路径
# <--- 使用默认方式，直接回车即可
Enter file in which to save the key (/home/reader/.ssh/id_rsa):
# <--- 自动创建密钥文件存放路径
Created directory '/home/reader/.ssh'.
# <--- 设置密码，该密码是每次使用密钥时需要的密码
# <--- 为了使用方便，直接回车不设密码
Enter passphrase (empty for no passphrase):
# <--- 使用默认方式，直接回车即可
Enter same passphrase again:
# <--- 此处说明私钥保存到~/.ssh/id_rsa文件中,该文件需要保密，不要让别人知道了
Your identification has been saved in /home/reader/.ssh/id_rsa.
# <--- 此处说明公钥保存到~/.ssh/id_rsa.pub文件中
Your public key has been saved in /home/reader/.ssh/id_rsa.pub.
# <--- 密钥指纹说明
The key fingerprint is:
SHA256:IZZxAMiKdj+z4QvGxOQfWfkN5xwf/r4vjzFAPTgJTdQ reader@ansible
# <--- 密钥随机图像
The key's randomart image is:
+---[RSA 2048]----+
| . ...o.. .+o.   |
|  o    +.  ..+E  |
|.. .  +o.. o=.o  |
|o.+. .o...*.+... |
|. .+.o  S. +.o   |
|  o .=.      ..  |
|   +..=       o. |
|  . .o        o+ |
|     ..       .==|
+----[SHA256]-----+
[reader@ansible ~]$
```



### 2.2 查看默认加密算法

可以使用`ssh-keygen`命令来查看，主要使用以下参数：

- `-f`， 指定密钥的路径。
- `-l`，显示密钥指纹信息。

```sh
# 显示id_rsa的指纹和所使用的加密算法
# 输出结果中，括号内的就是加密算法
[reader@ansible ~]$ ssh-keygen -l -f ~/.ssh/id_rsa
2048 SHA256:IZZxAMiKdj+z4QvGxOQfWfkN5xwf/r4vjzFAPTgJTdQ reader@ansible (RSA)

# 直接获取加密算法
[reader@ansible ~]$ ssh-keygen -l -f ~/.ssh/id_rsa|awk '{print $4}'|awk -F'[()]+' '{print $2}'
RSA
[reader@ansible ~]$
```

可以看到，默认是RSA加密算法。

可以看一下，`-t`参数：

> ```text
> -t dsa | ecdsa | ed25519 | rsa | rsa1
> 	Specifies the type of key to create.  The possible values are “rsa1” for protocol version 1 and “dsa”, “ecdsa”, “ed25519”, or “rsa” for protocol version 2.
> ```

可以通过`-t`参数指定生成密钥对时使用的加密算法。

在 SSH 中，常见的密钥类型包括以下几种：

- RSA：这是最早的 SSH 密钥类型之一，使用 RSA 加密算法。RSA 密钥在 SSH 中被广泛使用，并且是许多 SSH 工具和协议的默认密钥类型。

- DSA：这是另一种早期的 SSH 密钥类型，使用 DSA 加密算法。DSA 密钥已被广泛使用，但现在已不建议使用。

- ECDSA：这是一种基于椭圆曲线加密算法的 SSH 密钥类型，通常比 RSA 和 DSA 密钥更安全和高效。

- ed25519：这是一种基于椭圆曲线加密算法的公钥加密方案，它被广泛应用于 SSH 密钥认证。ed25519 密钥具有更高的安全性和更好的性能，因此在许多情况下被认为是最佳选择。

- ECIES：这是一种基于椭圆曲线加密算法的加密方案，可以在 SSH 中使用。ECIES 密钥通常用于加密和解密敏感数据。

**需要注意的是，不同的 SSH 工具和平台可能会支持不同的密钥格式和类型。在使用 SSH 密钥时，需要确保您的 SSH 工具支持您使用的密钥类型。**



后面我们再测试一下使用其他类型的加密算法。



### 2.3 查看默认密钥长度

生成密钥时，使用`-b`参数可以设置密钥长度（bits），默认是 2048 位。

> ```text
> -b bits
> 	Specifies the number of bits in the key to create.  For RSA keys, the minimum size is 1024 bits and the default is 2048 bits.  Generally, 2048 bits is considered sufficient.  DSA keys must be exactly 1024 bits as specified by FIPS 186-2.  For ECDSA keys, the -b
> 	flag determines the key length by selecting from one of three elliptic curve sizes: 256, 384 or 521 bits.  Attempting to use bit lengths other than these three values for ECDSA keys will fail.  Ed25519 keys have a fixed length and the -b flag will be ignored.
> ```

可以知道，对于RSA加密算法，默认是2048位。

- `-b`参数，指定要创建的密钥中的位数。对于RSA密钥，最小大小为1024位，默认值为2048位。通常，2048比特被认为是足够的。
- DSA密钥必须是FIPS 186-2指定的1024位。
- 对于ECDSA密钥，`-b`标志通过从三个椭圆曲线大小（256、384或521位）中选择一个来确定密钥长度。尝试将这三个值以外的位长度用于ECDSA密钥将失败。
- Ed25519加密具有固定长度，`-b`标志将被忽略。

我们可以像上一节一样，查看密钥文件所使用的密钥长度：

```sh
# 显示id_rsa的指纹和所使用的加密算法
# 输出结果中，最开始的数字是密钥长度
[reader@ansible ~]$ ssh-keygen -l -f ~/.ssh/id_rsa
2048 SHA256:IZZxAMiKdj+z4QvGxOQfWfkN5xwf/r4vjzFAPTgJTdQ reader@ansible (RSA)

# 直接获取密钥长度
[reader@ansible ~]$ ssh-keygen -l -f ~/.ssh/id_rsa|awk '{print $1}'
2048
[reader@ansible ~]$
```



### 2.4 指定加密算法和密钥长度生成密钥对

按以上两节说明指定算法和密钥长度，如使用椭圆曲线加密算法ECDSA，使用521位密钥。

#### 2.4.1 生成ecdsa密钥

```sh
# 使用椭圆曲线加密算法ECDSA，521位生成密钥
[reader@ansible ~]$ ssh-keygen -t ecdsa -b 521
Generating public/private ecdsa key pair.
Enter file in which to save the key (/home/reader/.ssh/id_ecdsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/reader/.ssh/id_ecdsa.
Your public key has been saved in /home/reader/.ssh/id_ecdsa.pub.
The key fingerprint is:
SHA256:+6jSHYmWyH6RDoMOjjlr9HgY4juxp9GmXfNFmgrGOrw reader@ansible
The key's randomart image is:
+---[ECDSA 521]---+
|                 |
|                 |
|                 |
|                 |
|   o . +So       |
|o++ = * *.       |
|B=BB O =.o       |
|+@O+= B oo       |
|oEO. +.o. .      |
+----[SHA256]-----+

# 此时，再查看密钥文件对应的加密算法是ECDSA，密钥长度521
[reader@ansible ~]$ ssh-keygen -l -f ~/.ssh/id_ecdsa
521 SHA256:+6jSHYmWyH6RDoMOjjlr9HgY4juxp9GmXfNFmgrGOrw reader@ansible (ECDSA)
[reader@ansible ~]$
```



#### 2.4.2 生成dsa密钥

```sh
# 生成一个长度为 1024 位的 DSA 密钥
[reader@ansible ~]$ ssh-keygen -t dsa -b 1024
Generating public/private dsa key pair.
Enter file in which to save the key (/home/reader/.ssh/id_dsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/reader/.ssh/id_dsa.
Your public key has been saved in /home/reader/.ssh/id_dsa.pub.
The key fingerprint is:
SHA256:RaPWiBSml+jfQGwBRLtbhY5JqJ0enVN2PUdWt/dSzh0 reader@ansible
The key's randomart image is:
+---[DSA 1024]----+
|   o+.=.  o o.. .|
|   . B = * +   ..|
|  . = @ * = .  Eo|
| o = % + . o   +=|
|. + O + S     . =|
| . . = o       . |
|  . . . .        |
|                 |
|                 |
+----[SHA256]-----+

# 查看密钥文件对应的加密算法和长度
[reader@ansible ~]$ ssh-keygen -l -f ~/.ssh/id_dsa
1024 SHA256:RaPWiBSml+jfQGwBRLtbhY5JqJ0enVN2PUdWt/dSzh0 reader@ansible (DSA)
[reader@ansible ~]$
```



#### 2.4.3 生成ed25519密钥

```sh
# 生成 ed25519 密钥
[reader@ansible ~]$ ssh-keygen -t ed25519
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/reader/.ssh/id_ed25519):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/reader/.ssh/id_ed25519.
Your public key has been saved in /home/reader/.ssh/id_ed25519.pub.
The key fingerprint is:
SHA256:RsVknEpFTqpBSv97PnGtHUhoOQQCi9JryckK547h8YE reader@ansible
The key's randomart image is:
+--[ED25519 256]--+
|    o.o .BB.     |
| . o = ..*=      |
|. o o o.oo.o     |
| + +   =. = .    |
|. O   . S. o o   |
|.=.    . .. o o  |
|oE..    . .o o . |
|.+o .    o. . .  |
|....      ..     |
+----[SHA256]-----+

# 查看密钥文件对应的加密算法和长度
# 可以看到ED25519算法的密钥长度是256位
[reader@ansible ~]$ ssh-keygen -l -f ~/.ssh/id_ed25519
256 SHA256:RsVknEpFTqpBSv97PnGtHUhoOQQCi9JryckK547h8YE reader@ansible (ED25519)
[reader@ansible ~]$ 
```



#### 2.4.4 简单获取密钥算法信息

通过以上三节，可以看到，默认会在`~/.ssh`目录下生成公钥和私钥文件，我们可以看一下文件列表：

```sh
[reader@ansible ~]$ ll .ssh/
total 32
-rw-------. 1 reader reader  668 Jan 13 21:14 id_dsa
-rw-r--r--. 1 reader reader  604 Jan 13 21:14 id_dsa.pub
-rw-------. 1 reader reader  365 Jan 13 21:02 id_ecdsa
-rw-r--r--. 1 reader reader  268 Jan 13 21:02 id_ecdsa.pub
-rw-------. 1 reader reader  411 Jan 13 21:17 id_ed25519
-rw-r--r--. 1 reader reader   96 Jan 13 21:17 id_ed25519.pub
-rw-------. 1 reader reader 1679 Jan 11 06:51 id_rsa
-rw-r--r--. 1 reader reader  396 Jan 11 06:51 id_rsa.pub
[reader@ansible ~]$
```

可以看到，生成了4种类型的公钥和密钥文件。可以通过密钥文件名简单判定该密钥文件对应的加密算法。

如`id_rsa`对应的加密算法是`RSA`，`id_ecdsa`对应的加密算法是椭圆曲线加密算法`ECDSA`。



当然，这种方式不一定准确，如自定义公钥和密钥文件名称时，使用该方法就不行了。请看下节。



### 2.5 指定密钥名称

可以使用`ssh-keygen`命令的`-f`参数， 指定密钥的路径。

```sh
# 生成密钥时，指定密钥文件路径和名称
[reader@ansible ~]$ ssh-keygen -f ~/.ssh/id_secure
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/reader/.ssh/id_secure.
Your public key has been saved in /home/reader/.ssh/id_secure.pub.
The key fingerprint is:
SHA256:XBuigdQpxS8yGUlqTuyxwrrklIUeRBzq0BYFLmF6Zuk reader@ansible
The key's randomart image is:
+---[RSA 2048]----+
|o++++=..         |
|=* =+.+          |
|=.# .+... o      |
|=%.o+ .+.o o     |
|.=E. o..S .      |
|o.+              |
|.=               |
|+.               |
|..               |
+----[SHA256]-----+
[reader@ansible ~]$ 
```

此时，查看新生成的密钥和公钥文件信息：

```sh
[reader@ansible ~]$ ll ~/.ssh/id_secure*
-rw-------. 1 reader reader 1679 Jan 14 07:33 /home/reader/.ssh/id_secure
-rw-r--r--. 1 reader reader  396 Jan 14 07:33 /home/reader/.ssh/id_secure.pub
[reader@ansible ~]$
```

此时，公钥名称是`id_secure.pub`，私钥名称是`id_secure`,通过文件名是不能直接判断出加密算法是什么的。

而通过2.2节的方式还是能够正常获取到的：

```sh
[reader@ansible ~]$ ssh-keygen -l -f ~/.ssh/id_secure
2048 SHA256:XBuigdQpxS8yGUlqTuyxwrrklIUeRBzq0BYFLmF6Zuk reader@ansible (RSA)
[reader@ansible ~]$
```

可以看到`id_secure`对应的加密算法是`RSA`。





### 2.6 指定公钥备注信息

可以通过`-C`参数指定生成公钥时使用的备注信息。

```
-C comment
	Provides a new comment.

-c      Requests changing the comment in the private and public key files.  This operation is only supported for RSA1 keys and keys stored in the newer OpenSSH format.  The program will prompt for the file containing the private keys, for the passphrase if the key has one, and for the new comment.
```

查看公钥文件信息：

```sh
[reader@ansible ~]$ cat ~/.ssh/id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzJyZebpf5k4KdYvJKRT4VfhLsbR/xz5QeNw3CHidihzZpPy851sTwPrEUKG46FTUDYDKWWWMsZ8OwTcdtKaccXbBfUU5pnvqrqON0CL3sWUpEuMokutp7AZNGzPM02/Vh4Z319yDTtMi1fq5DFOlymy5x6Jz7pLV+0jWoqTUiRwI9Ma35QtX/lYkbZDGclpbcYpDWVodDhwKFWT6on6vczrtyRhiQ+KZfhg6YN1kJud2BK/1Ya6D/ACy+x3fGkNJH+fGfAE7F6GvLX+Uhgr/DggYzXHXRtUGzKf4wEJUA2jTxXwMk8gEIoPHTkkECazcm0I4McvTOF0TUSFFso6Pb reader@ansible
[reader@ansible ~]$ cat ~/.ssh/id_dsa.pub
ssh-dss AAAAB3NzaC1kc3MAAACBAI+vnkwRwqDoZ/xIAARyZjDtuZdNj5DxlnzJPadZLGsTX363RSEpRLHJ10FdGeJPN+pQ1N8rOvMyvLl6F3JMBKjEsW9BeC1R+mjcAUg7UUeTQgUXQS7CNchcsWrRQrCyYsNQ4/zucoTyWjW1zJQqUSQzhAWZhbDPx9nZishBNVlFAAAAFQCjyt6g+KmwGQDnMN3uEJchka5ZNQAAAIBanchtzSinMPdeIjMuN97cfv9vz8VOMd1aDnXomKe7RNCXIWQ6Pi4+UTGUqP09nKkPubNBoZOkfwPqQF5y5Rl66izRCvN1pxMWEJXfc5Ya0JOACU+0zd9f52wmCm62p4vLW249Hjyi8Sy9uVgmiyRk9rVYreVQg049etf/fb4KeQAAAIBjXIrU6W4vpT1ZPmf4YKGxj3WXrMbKp4cw/yKuztx2x91CBk5b0BVrbfT93QmHvQ20wfOst+tz0sSF+4przP7Tzq/m/baxKdyvkuxZzuYNbL+dSrcKqka9A8uL9+Jj2CkxeHjY1aszsQsWCo94HALlT67eQbl+Eb4J3iw6FLGw2w== reader@ansible
[reader@ansible ~]$ cat ~/.ssh/id_ecdsa.pub
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBACkcn1Luxdn3W3QO8yeOw1uQsM3RsubT7k2LT9R0GYqgD1gdyWDlr4nSrgC9HEV2LY4hlmY/iiGWdYMuq6/c82A3wGG51+5GR5IM44LGvCyu6ux//TpZEnCsIcY4qwRd9S7pmIrhJTl8L0M8Rrt2ZNM2EgcQqNa+3UAvMLW7J7JWbnRrw== reader@ansible
[reader@ansible ~]$ cat ~/.ssh/id_ed25519.pub
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINyxt2lpb9KJWy1pAWClGAVhdiH3GfVv8JYR65L4sjLz reader@ansible
[reader@ansible ~]$
```

可以看到，4种类型的备注信息都是`reader@ansible`。



为了更好的区分是哪个服务器上面的公钥，通常建议直接使用 `${USERNAME}@${IP}`这种形式，即用户名@IP地址。



#### 2.6.1 修改已经存在的公钥密钥的备注信息

假如我要对`~/.ssh/id_secure.pub`公钥的备注信息进行修改。

查看当前主机的IP信息：

```sh
[reader@ansible ~]$ hostname -I
192.168.56.120 10.0.3.15
[reader@ansible ~]$
```

IP是`192.168.56.120`，那我的备注信息应该是`reader@192.168.56.120`。



为了测试修改备注信息时，配置文件公钥和密钥信息是否会发生变化，我们先进行一下备份：

```sh
# 备份
[reader@ansible ~]$ cp -p ~/.ssh/id_secure.pub ~/.ssh/id_secure.pub.bak
[reader@ansible ~]$ cp -p ~/.ssh/id_secure ~/.ssh/id_secure.bak

# 查看备份文件
[reader@ansible ~]$ ll ~/.ssh/id_secure*
[reader@ansible ~]$ ll ~/.ssh/id_secure*
-rw-------. 1 reader reader 1679 Jan 14 07:33 /home/reader/.ssh/id_secure
-rw-------. 1 reader reader 1679 Jan 14 07:33 /home/reader/.ssh/id_secure.bak
-rw-r--r--. 1 reader reader  396 Jan 14 07:33 /home/reader/.ssh/id_secure.pub
-rw-r--r--. 1 reader reader  396 Jan 14 07:33 /home/reader/.ssh/id_secure.pub.bak
-rw-r--r--. 1 reader reader  396 Jan 11 06:51 /home/reader/.ssh/id_rsa.pub.bak
[reader@ansible ~]$
```



我们进行修改：

```sh
# 修改备注信息
[reader@ansible ~]$ ssh-keygen -c -C "reader@192.168.56.120" -f ~/.ssh/id_secure
Comments are only supported for RSA1 or keys stored in the new format (-o).
```
可以看到，报异常了`Comments are only supported for RSA1 or keys stored in the new format (-o).`,即注释仅支持RSA1或以新格式（-o）存储的密钥。

> ```text
>  -o Causes ssh-keygen to save private keys using the new OpenSSH format rather than the more compatible PEM format.  The new format has increased resistance to brute-force password cracking but is not supported by versions of OpenSSH prior to 6.5.  Ed25519 keys always use the new private key format.
> ```

即：使ssh keygen使用新的OpenSSH格式而不是更兼容的PEM格式保存私钥。新格式增加了对暴力破解密码的抵抗力，但6.5之前的OpenSSH版本不支持。Ed25519私钥始终使用新的私钥格式。

```sh
# 查看OpenSSH版本信息
[reader@ansible ~]$ ssh -V
OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017
```

可以看到版本是`OpenSSH_7.4p1`，支持新格式存储密钥。



我们增加`-o`参数再试下：

```sh
[reader@ansible ~]$ ssh-keygen -c -C "reader@192.168.56.120" -f ~/.ssh/id_secure -o
Key now has comment '(null)'
The comment in your key file has been changed.
[reader@ansible ~]$
```

可以看到，备注更新成功。对比一下备份文件：
```sh
[reader@ansible ~]$ diff ~/.ssh/id_secure ~/.ssh/id_secure.bak -y
[reader@ansible ~]$ diff ~/.ssh/id_secure.pub ~/.ssh/id_secure.pub.bak
```

效果图：

![](/img/Snipaste_2024-01-14_08-46-59.png)

可以看到，密钥文件`~/.ssh/id_secure`发生了变化，公钥文件除了最后备注信息不一样，前面的字符串没有发生变化。

OpenSSH 创建了自己的存储私钥的格式（带有`BEGIN OPENSSH PRIVATE KEY`标头的格式），该格式使用与 SSH 本身相同的结构和算法标识符。



对比备份文件和新文件中的备注信息：

```sh
[reader@ansible ~]$ ssh-keygen -l -f ~/.ssh/id_secure.bak
2048 SHA256:XBuigdQpxS8yGUlqTuyxwrrklIUeRBzq0BYFLmF6Zuk no comment (RSA)
[reader@ansible ~]$ ssh-keygen -l -f ~/.ssh/id_secure
2048 SHA256:XBuigdQpxS8yGUlqTuyxwrrklIUeRBzq0BYFLmF6Zuk reader@192.168.56.120 (RSA)
```

旧的备份密钥文件中没有备注信息，新的密钥文件中有备注信息。



可以通过以下命令来查看密钥对应的十六进制的字符串信息：

```sh
[reader@ansible ~]$ cat ./.ssh/id_secure|grep -v '\-\-' |base64 -d|hexdump -C|tail
00000490  ca 3a 1b 1e e8 f4 f4 ef  95 36 8c 6f a3 60 85 86  |.:.......6.o.`..|
000004a0  e6 d8 d1 1d 9a 80 80 8f  5f 9a f9 64 c1 1b 10 ee  |........_..d....|
000004b0  05 65 5a 1b 1d c1 35 85  c1 d1 f4 d6 17 ae ad 0b  |.eZ...5.........|
000004c0  1a f3 9c f2 ee c6 f1 6b  f4 43 34 1d d6 9d b1 fa  |.......k.C4.....|
000004d0  bb ac 41 a4 bc c8 0b 34  52 51 fd d3 94 64 40 10  |..A....4RQ...d@.|
000004e0  91 b0 d2 aa 65 aa 70 df  bd 86 85 d4 9b 25 61 e7  |....e.p......%a.|
000004f0  fb e8 76 aa 93 37 86 5b  d1 00 00 00 15 72 65 61  |..v..7.[.....rea|
00000500  64 65 72 40 31 39 32 2e  31 36 38 2e 35 36 2e 31  |der@192.168.56.1|
00000510  32 30 01 02 03 04                                 |20....|
00000516
[reader@ansible ~]$ cat ./.ssh/id_secure.bak|grep -v '\-\-' |base64 -d|hexdump -C|tail
00000420  00 29 35 59 51 02 81 81  00 c3 67 6f 50 d2 29 ae  |.)5YQ.....goP.).|
00000430  a2 e4 50 a6 35 ac f4 73  94 8a aa 22 75 ef dd 54  |..P.5..s..."u..T|
00000440  17 66 51 83 1d 22 4e 5a  8d 94 3c 14 a5 12 a9 ff  |.fQ.."NZ..<.....|
00000450  27 2f cd 6f 27 7c 45 c7  40 d7 e9 1c 1c db 48 39  |'/.o'|E.@.....H9|
00000460  8d 40 ac fd 98 a3 e6 49  f7 64 fb ff 5d 0f 8b f8  |.@.....I.d..]...|
00000470  be dd a0 25 ad 7d 38 f3  0d 90 39 79 4d 75 6d f5  |...%.}8...9yMum.|
00000480  9c 53 6b f6 54 a7 19 3a  8f a0 31 d5 fa 6d fb ce  |.Sk.T..:..1..m..|
00000490  57 81 df e8 05 0e fe b1  15 70 21 89 bd 3e cb 85  |W........p!..>..|
000004a0  55 89 4c ff 7e a3 03 48  42                       |U.L.~..HB|
000004a9
```

为了避免输出字符太长， 此处在命令后面加了`tail`只取最后10行。

![](/img/Snipaste_2024-01-14_09-23-13.png)

可以从新格式的十六进制的字符串信息看到新增加的备份信息。



由于该方法使用了新格式的加密算法，可能导致某些不兼容，当我们公钥已经发出去很多时，就不建议再通过这种方式修改公钥备注，导致密钥格式发生变化。



#### 2.6.2 仅修改公钥中的备注信息



如果仅想修改公钥中的备注修改，可以直接修改公钥文件`~/.ssh/id_sercure.pub`文件。

直接使用`vim`编辑器，或者`sed`命令替换即可。

```sh
# 查看备份文件
[reader@ansible ~]$ cat ~/.ssh/id_secure.pub.bak
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxJk0idL8t6c4oCo9Kd7vQO2iop0Cu/dUFgn0BJGTLPFt5WpwX90/wovHF8kiT2W7f44/oQeKAfM18zSxr4myK4b9wkzut8Phxk/60OX8t5RMloBQHt8qgjR4YmkRkcNGkZVRX1+hk59hjXxbxo+Sq/mUpdKyn61547RKK8td706dMlRUlgOGfPAr4CeewP4HbKGqZkkQWGsvss3FvPR5j7YgmvInXa40NBy/P2kP3EeWsYEtWO4BxIfh+rx3I3TwsZfciD1FmVHINm0Xn+ZYUHMSkyi09RyLkVowG7344BKXPVe741KBFjCeIQNWRCL61yhjX2BgBJj9SSNZtTFyN reader@ansible

# 查看修改后的文件
[reader@ansible ~]$ cat ~/.ssh/id_secure.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxJk0idL8t6c4oCo9Kd7vQO2iop0Cu/dUFgn0BJGTLPFt5WpwX90/wovHF8kiT2W7f44/oQeKAfM18zSxr4myK4b9wkzut8Phxk/60OX8t5RMloBQHt8qgjR4YmkRkcNGkZVRX1+hk59hjXxbxo+Sq/mUpdKyn61547RKK8td706dMlRUlgOGfPAr4CeewP4HbKGqZkkQWGsvss3FvPR5j7YgmvInXa40NBy/P2kP3EeWsYEtWO4BxIfh+rx3I3TwsZfciD1FmVHINm0Xn+ZYUHMSkyi09RyLkVowG7344BKXPVe741KBFjCeIQNWRCL61yhjX2BgBJj9SSNZtTFyN reader@192.168.56.120
```

即直接将`~/.ssh/id_secure.pub`最后的信息`reader@ansible`修改成` reader@192.168.56.120`即可。



#### 2.6.3 在创建公钥密钥对时指定备注信息

创建`-C`参数，直接指定备注信息：

```sh
[reader@ansible ~]$ ssh-keygen -C reader@192.168.56.120 -f ~/.ssh/id_rsa_with_public_comment
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/reader/.ssh/id_rsa_with_public_comment.
Your public key has been saved in /home/reader/.ssh/id_rsa_with_public_comment.pub.
The key fingerprint is:
SHA256:AGs2bKi+cYJjTSn2Q8MHzVKnZ+Hq568WwPbyB4cx73s reader@192.168.56.120
The key's randomart image is:
+---[RSA 2048]----+
|    .. o         |
|   o+o+ .        |
|  .oO+.+         |
| ..++=++         |
|.o *.oo S        |
|+ * +. = o       |
|o= = .o.=        |
|..= . oo o E     |
| .    .o+oo      |
+----[SHA256]-----+

# 查看新生成的公钥和密钥文件
[reader@ansible ~]$ ll ~/.ssh/id_rsa_with_public_comment*
-rw-------. 1 reader reader 1675 Jan 14 09:39 /home/reader/.ssh/id_rsa_with_public_comment
-rw-r--r--. 1 reader reader  403 Jan 14 09:39 /home/reader/.ssh/id_rsa_with_public_comment.pub

# 查看公钥文件里面的备注信息
[reader@ansible ~]$ cat /home/reader/.ssh/id_rsa_with_public_comment.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAanIO3lNVCoKCe7SloudfZopLBW2/MljGcJsS/068gZAFB2p+WGjZLDKbAMDOzIbePrBSalpsTybtO1cLPAnIZYoGwXDMh7k7Z2OcKXCHfbLEiw5DCGJDNHaPDNa2PmmK9WRjxdgoqWu7VqsQ8DjJyASmzJm/1VhQl8rlzOLO5fKFMbsGuC0u45Eq9CgU0rqN07AcgGKyNxW1e0ORFUAXuMbsAn5sH6Llj2K9Yvc/PYqXr0AbbEeQdbwhIxuReDThPF+rVV9tP6u3sRzXrAylziAQZjq8+rExF+MG72eQz7ORV92772NEYbDvGd5K0Mkv3euQUvvQXR59vr+T/quj reader@192.168.56.120
[reader@ansible ~]$
```



### 2.7 创建密钥时设置密码

#### 2.7.1 创建密钥时设置密码

本节主要使用以下参数：

```
-N new_passphrase
	Provides the new passphrase.
-y      This option will read a private OpenSSH format file and print an OpenSSH public key to stdout.
-P passphrase
 	Provides the (old) passphrase.
 -p      Requests changing the passphrase of a private key file instead of creating a new private key.  The program will prompt for the file containing the private key, for the old passphrase, and twice for the new passphrase.
```

- `-N`，设置密钥使用的新密码。
- `-y`，读取密钥文件，并输出公钥信息到控制台。
- `-P`，大写`P`，提供旧的密钥密码。
- `-p`，小写`p`，修改密钥的密码。



创建密钥时，指定密钥的密码为`passwd`：

```sh
# 创建密钥时，通过`-N`参数指定密码
[reader@ansible ~]$ ssh-keygen -C reader@192.168.56.120 -N "passwd" -f ~/.ssh/id_rsa_with_password
Generating public/private rsa key pair.
Your identification has been saved in /home/reader/.ssh/id_rsa_with_password.
Your public key has been saved in /home/reader/.ssh/id_rsa_with_password.pub.
The key fingerprint is:
SHA256:QCpZXSDrIpPvVrYhHc9WACtBjGM5DSpQU0vOHIiXf7M reader@192.168.56.120
The key's randomart image is:
+---[RSA 2048]----+
|.BO+Booo.        |
|*+=@ Oo          |
|+o=.O ..         |
|.. +o o..        |
|+ ...= +S        |
| +..= E          |
|  .+ +           |
| .. .            |
| ..              |
+----[SHA256]-----+

# 有密码保护的私钥，配置文件前4行与没有密码保护的不一样
[reader@ansible ~]$ cat ~/.ssh/id_rsa_with_password
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,C2E4BF881A3DEDA3ECF1790DFE258832

x3GeGxcs4MWkVLTfFkcUPn45VLI6ZN/I/xEehRNnd9DLn98VlExZBQ4QydAY5MDW
hHtIEpxNsICsgFVrM6gkg7a67Y8XCNRRTrkXM9urfFTmOugJn/BQMqAksaJmLba+
b9pqSTQeVc/1aDOrvR6EfrOaGZbOHuaKn+mRjW0RMC/xa9OKXZwiZTT+JBBZ32fV
ZHaQu9h1w0jbm2bm3YcEe1JO5IboejSqPWKiVNQx3FCD3LUpPOxPS/27iw8LehTu
unJqtsk3rISF7QH+nMQRduRPH0GVMrTaSC/Ib9nhfifLc7u6wsr1u8VCcDvxX+ah
gq5HSdOZrcQtgq+ILUg/ZZfXXMoeqJL4BR3bFljn9D+4xKCK+qlsVBuTryH4CjgR
049WIWHz6JSeu0jlRwZN28ndSHlH1fFZ5Cyyx5U51XGLJDLGRlkEsqQpC0Li5lhZ
1Seu0ll92gBbQj+M6whdTLysR3YYAV5Dkknrs6vA2PYsGfeg5IHUoL6qYKtdk4kE
n9sXNPLoGWhZ7zOLI9zUC36zPx4Lx6iqw2WU2ow48cLOTQCHiqS1zJGwbeYQdy2b
ssmwzzM5NlkxsB3Qt0EHzewohg8D8P8YBIXpyOFhWayk5LWFbPrCd3b3P8aQcoI2
Yuz4ehyuC+0IAyMh4qPxFIxqZxz3huzr+UmYxBS25h+A0x9s8II2tnLBCSfOpMsw
KslH9BbgRYJCsV6Njyb9TXdl+6YRBsxZUjRz0PB6QW0qjd5FstL1gbdbYPUKi1Np
R6H1pPQDuBUVe/re4BocQRrn592d6HyckNHHcLK/ihSuAedvHq+uFyETRNGHeGgM
F1Q+aCdtxTZYJa6SaVEK8Qh5tFQ2GlQoD2kLMNE1l2g9tVHF1pmUB9oKfOsUCsdu
W79TS8fiCOWhR22wCJSsG9c3JI1MD5L2JA9U3HsZ+6gKTwT4Pd8JjLuJqU3Gs+34
/SIot1V9IFLi0k2R/E/BuqEBFaY8HxbFAg2RAJUpk6XPdjEkuwmHe8MeqMKdNypA
u+5KPHWBG1ChXuIftMnQxxvZyNjdvM+Woq5JbPb4Du+5has6XeKkLIFwMoiDa+TR
X3+LFO44+YezxdUeSV/2FvZGhphrC4HrxoDTOzWY6MLB9kCIhPrVjXhBYO5spR7r
O2YQ0O7Ilsms8pIE/Nx6pmTXag6ZbXYOeqiRlKG3PwiBbMvhMADbkXSFi8owoj4Z
Af6iXPbNJykTN2GzExagE7ADNaStcwNgdoEqsimgyOnvWeTBeA7YOzMPNfUvHEDj
ypZgd85LBVbHO6qP0ks31z3oYBOlPfVtdabHQc7y+rgneB6OS33RtVusjd5NMCDs
0XrlOIJ68Gl36j7JYPh4WAxWDccsmCYj1gDELJ2mT+aJ1ierLUQJ2pIXS3k2hVqa
2CyYW3AStjIopfC8QPLlG2VP0pQAxJ6prhj025QIMYFHIAAOm92aOhRyZPvB8I0k
fQQ/5YP+XvjqkZaRbiUFvPvRix3F5WN/fuFLk0QPOc/VeMGmLQ5M2ADegUKMM+Qd
508zn/ZaWmRroeqFbj2vK6WaoY1Buo9KGAa0VrkHfdtq9TI/EnFaC/mHKVhoTd60
-----END RSA PRIVATE KEY-----
[reader@ansible ~]$
```

密钥文件中，第2行中包含`ENCRYPTED`，说明密钥文件已经有密码保护。



#### 2.7.2 检查密钥是否有密码保护

检查密钥文件是否有密码保护：

```sh
# 读取密钥文件，由于密码输入错了，显示incorrect passphrase不正确的密码异常
[reader@ansible ~]$ ssh-keygen -y -f ~/.ssh/id_rsa_with_password
Enter passphrase:
Load key "/home/reader/.ssh/id_rsa_with_password": incorrect passphrase supplied to decrypt private key

# 读取密钥文件，正确输入密码passwd后，正常显示出了公钥信息
[reader@ansible ~]$ ssh-keygen -y -f ~/.ssh/id_rsa_with_password
Enter passphrase:
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDGr0GOEFhbJVvLjgL14OO8jQbuIZP75rmHGBhYrgM2FM2VQX48lnK+Kzl5jxWpSliYfwRhxdcoFZOfV5+vf3UL4Rez69Ao1T3sNoGm1ygpqtBCoHeGTUbuiLld8uHWeyZ7ZNEd6KkmNRfLFbKldpM0wkEYPd2oiH8bEwZ/syLkZgPsexzpot9GQ9mGJm8OdHTXg0iH3r2mr1WlTTzF3f5583nLI/IZqUjWFpdZN2/k8dFlw2NL6gPGSHICyvqFLqiCBjde2BQiVpf1IZLJqsyiwWZcmYHuV6geKoe8PyA6x9KJZD/5iTnv/FnQ0mCUJLCnfPwUAfLvJJwBx8OJksgL
[reader@ansible ~]$
```



### 2.8 非交互模式生成密钥对

之前创建密钥时，都会在交互模式下生成密钥对，为了不进入交互模式，需要使用`-q`参数：

```
-q      Silence ssh-keygen.
```

非交互模式下创建无密码的密钥对：

```sh
# 使用`-q`参数则会非交互模式下生成密钥文件
[reader@ansible ~]$ ssh-keygen -C reader@192.168.56.120 -N "" -q -f ~/.ssh/id_rsa_without_password

# 检查刚生成的文件
[reader@ansible ~]$ ll ~/.ssh/id_rsa_without_password*
-rw-------. 1 reader reader 1675 Jan 14 11:34 /home/reader/.ssh/id_rsa_without_password
-rw-r--r--. 1 reader reader  403 Jan 14 11:34 /home/reader/.ssh/id_rsa_without_password.pub
[reader@ansible ~]$
```

可以看到，此时`ssh-keygen`已经静默生成了新的密钥文件了。



## 3. 免密登陆远程主机

### 3.1 使用ssh-copy-id复制公钥到远程主机

尝试使用`ssh-copy-id`复制公钥到远程主机：

```sh
# 复制公钥
[reader@ansible ~]$ ssh-copy-id root@192.168.56.121
/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/reader/.ssh/id_rsa_without_password.pub"
/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
root@192.168.56.121's password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'root@192.168.56.121'"
and check to make sure that only the key(s) you wanted were added.
```
可以看到，公钥已经复制到远程主机了。


尝试无密码登陆远程主机：

```sh
[reader@ansible ~]$ ssh 'root@192.168.56.121'
root@192.168.56.121's password:
```

但仍然需要输入密码。



原因，在SSH 2协议中，`ssh`命令默认会读取~/.ssh/id_dsa, ~/.ssh/id_ecdsa, ~/.ssh/id_ed25519 和 ~/.ssh/id_rsa这几个密钥文件：

```
-i identity_file
	Selects a file from which the identity (private key) for public key authentication is read.  The default is ~/.ssh/identity for protocol version 1, and ~/.ssh/id_dsa, ~/.ssh/id_ecdsa, ~/.ssh/id_ed25519 and ~/.ssh/id_rsa for protocol version 2.  Identity files may also be specified on a per-host basis in the configuration file.  It is possible to have multiple -i options (and multiple identities specified in configuration files).  If no certificates have been explicitly specified by the CertificateFile directive, ssh will also try to load certificate information from the filename obtained by appending -cert.pub to identity filenames.
```



登陆时指定密钥文件：

```sh
# 登陆远程时指定密钥文件
[reader@ansible ~]$ ssh 'root@192.168.56.121' -i ~/.ssh/id_rsa_without_password
Last login: Sun Jan 14 12:05:27 2024 from 192.168.56.120
[root@ansible-node1 ~]# whoami
root
[root@ansible-node1 ~]# hostname -I
192.168.56.121 10.0.3.15
[root@ansible-node1 ~]# 
```

此时，可以正常免密登陆到远程主机。



### 3.2 ssh-copy-id不进入交互模式

直接使用`ssh-copy-id`复制公钥到远程主机的时候，需要输入远程主机密码。如果不想手动输入密码，可以使用`sshpass`工具。详细使用方法参考第4章。

```sh
# 复制公钥前，登录远程主机需要输入密码，按Ctrl+C取消
[reader@ansible ~]$ ssh root@192.168.56.121
root@192.168.56.121's password:


# 非交互是复制公钥到远程主机，可以看到中间不要手动输入密码，公钥就复制到远程主机了
[reader@ansible ~]$ SSHPASS=123456 sshpass -e ssh-copy-id root@192.168.56.121
/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/reader/.ssh/id_rsa.pub"
/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'root@192.168.56.121'"
and check to make sure that only the key(s) you wanted were added.

# 尝试登录远程主机，可以看到不需要输入密码了
[reader@ansible ~]$ ssh 'root@192.168.56.121'
Last login: Mon Jan 15 06:27:19 2024 from 192.168.56.1
[root@ansible-node1 ~]# whoami
root
[root@ansible-node1 ~]# hostname -I
192.168.56.121 10.0.3.15
[root@ansible-node1 ~]# ll ~/.ssh/authorized_keys
-rw------- 1 root root 804 Jan 18 06:54 /root/.ssh/authorized_keys
[root@ansible-node1 ~]# exit
logout
Connection to 192.168.56.121 closed.
[reader@ansible ~]$
```





## 4. sshpass的使用

`sshpass`工具。

> The `sshpass` utility is designed to run SSH using the *keyboard-interactive* password authentication mode, but in a non-interactive way.
>
> SSH uses direct TTY access to ensure that the password is indeed issued by an interactive keyboard user. `sshpass` runs SSH in a dedicated TTY, fooling SSH into thinking it is getting the password from an interactive user.

sshpass会在一个专用的`TTY`中运行SSH，欺骗SSH以为它是从交互式用户那里获取密码。

如果没有`sshpass`命令，则可以使用`root`账号安装一下：

```sh
[root@ansible ~]# yum install sshpass
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
...省略
Package sshpass-1.06-2.el7.x86_64 already installed and latest version
Nothing to do
[root@ansible ~]# rpm -qa|grep sshpass
sshpass-1.06-2.el7.x86_64
```



查看帮助信息：

```sh
[reader@ansible ~]$ sshpass -h
Usage: sshpass [-f|-d|-p|-e] [-hV] command parameters
   -f filename   Take password to use from file
   -d number     Use number as file descriptor for getting password
   -p password   Provide password as argument (security unwise)
   -e            Password is passed as env-var "SSHPASS"
   With no parameters - password will be taken from stdin

   -P prompt     Which string should sshpass search for to detect a password prompt
   -v            Be verbose about what you're doing
   -h            Show help (this screen)
   -V            Print version information
At most one of -f, -d, -p or -e should be used
[reader@ansible ~]$
```



为了测试`sshpass`命令的使用，我们将`~/.ssh`中之前创建的测试密钥文件都删除掉。并清理到node1上面的`authorized_keys`文件中的公钥信息。

```sh
[reader@ansible ~]$ rm -rf ~/.ssh/*
[reader@ansible ~]$ ll ~/.ssh/
total 0
[reader@ansible ~]$
```

重新生成一个不带密码的密钥对：

```sh
[reader@ansible ~]$ ssh-keygen -C reader@192.168.56.120 -N "" -q -f ~/.ssh/id_rsa
[reader@ansible ~]$ ll ~/.ssh/
total 8
-rw-------. 1 reader reader 1675 Jan 14 13:38 id_rsa
-rw-r--r--. 1 reader reader  403 Jan 14 13:38 id_rsa.pub
[reader@ansible ~]$
```



### 4.1 -p参数直接在命令行指定密码

尝试SSH到远程主机：

```sh
[reader@ansible ~]$ sshpass -p 123456 ssh root@192.168.56.121
Last login: Sun Jan 14 13:40:30 2024 from 192.168.56.120
[root@ansible-node1 ~]# exit
logout
Connection to 192.168.56.121 closed.
[reader@ansible ~]$ sshpass -p 123456 ssh root@192.168.56.121
Last login: Sun Jan 14 13:40:46 2024 from 192.168.56.120
[root@ansible-node1 ~]# hostname -I
192.168.56.121 10.0.3.15
[root@ansible-node1 ~]# who
root     pts/0        2024-01-14 10:25 (192.168.56.1)
root     pts/1        2024-01-14 13:41 (192.168.56.120)
[root@ansible-node1 ~]# exit
logout
Connection to 192.168.56.121 closed.
[reader@ansible ~]$
```

可以看到，自动读取到了密码`123456`，并成功连接到远程主机了。



### 4.2 -f参数从文件中读取密码

也可以将密码写入到密码文件中，然后从文件中读取密码：



直接将密码写入到文件`.pass_file`中，然后通过指定`-f`参数，从文件中读取密码：

```sh
[reader@ansible ~]$ echo '123456' > .pass_file
[reader@ansible ~]$ sshpass -f .pass_file  ssh root@192.168.56.121
Last login: Sun Jan 14 13:41:00 2024 from 192.168.56.120
[root@ansible-node1 ~]# hostname -I
192.168.56.121 10.0.3.15
[root@ansible-node1 ~]# exit
logout
Connection to 192.168.56.121 closed.
[reader@ansible ~]$
```

为了密码文件的安全，应修改其权限，禁止其他用户查看：

```sh
[reader@ansible ~]$ ls -lah .pass_file
-rw-rw-r--. 1 reader reader 7 Jan 14 13:45 .pass_file
[reader@ansible ~]$ chmod 600 .pass_file
[reader@ansible ~]$ ls -lah .pass_file
-rw-------. 1 reader reader 7 Jan 14 13:45 .pass_file
[reader@ansible ~]$
```

这样其他用户就没有读取密码文件的权限了。



### 4.3 -e指定环境变量SSHPASS

也可以骑过`SSHPASS`指定环境变量，配合`sshpass -e`来使用：

```sh
[reader@ansible ~]$ SSHPASS=123456 sshpass -e ssh root@192.168.56.121
Last login: Sun Jan 14 13:45:19 2024 from 192.168.56.120
[root@ansible-node1 ~]# hostname -I
192.168.56.121 10.0.3.15
[root@ansible-node1 ~]# exit
logout
Connection to 192.168.56.121 closed.
[reader@ansible ~]$
```

可以看到，同样登陆成功了。



### 4.4 rsync和scp中使用sshpass

rsync同步命令中使用sshpass:

> Use `sshpass` with `rsync`:
>
> ```shell
> $ SSHPASS='!4u2tryhack' rsync --rsh="sshpass -e ssh -l username" /custom/ host.example.com:/opt/custom/ 
> ```
>
> The above uses the `-e` option, which passes the password to the environment variable **SSHPASS**
>
> We can use the `-f` switch like this:
>
> ```shell
> $ rsync --rsh="sshpass -f pass_file ssh -l username" /custom/ host.example.com:/opt/custom/
> ```



示例：

```sh
# 通过环境变量方式同步文件
[root@ansible ~]# SSHPASS='123456' rsync --rsh="sshpass -e ssh -l root" /root/ssh-keygen.man.txt 192.168.56.121:/root/ssh-keygen.man.txt.byenv

# 通过密码文件方式同步文件
[root@ansible ~]# rsync --rsh="sshpass -f .pass_file ssh -l root" /root/ssh-keygen.man.txt 192.168.56.121:/root/ssh-keygen.man.txt.byfile
[root@ansible ~]#
```



在远程主机192.168.56.121上面查看复制过去的文件：

```sh
[root@ansible-node1 ~]# ll ssh-keygen.man.txt*
-rw-r--r-- 1 root root 26349 Jan 15 06:34 ssh-keygen.man.txt.byenv
-rw-r--r-- 1 root root 26349 Jan 15 06:34 ssh-keygen.man.txt.byfile
[root@ansible-node1 ~]#
```

可以看到，文件正常同步到远程主机。





scp复制时使用sshpass:

> Use `sshpass` with `scp:`
>
> ```shell
> $ scp -r /var/www/html/example.com --rsh="sshpass -f pass_file ssh -l user" host.example.com:/var/www/html
> ```

在scp中也可以使用sshpass。



### 4.4  GPG加密密码文件

> You can also use `sshpass` with a GPG-encrypted file. When the `-f` switch is used, the reference file is in plaintext. Let's see how we can encrypt a file with GPG and use it.
>
> First, create a file as follows:
>
> ```shell
> $ echo '!4u2tryhack' > .sshpasswd
> ```
>
> Next, encrypt the file using the `gpg` command:
>
> ```shell
> $ gpg -c .sshpasswd
> ```
>
> Remove the file which contains the plaintext:
>
> ```shell
> $ rm .sshpasswd
> ```
>
> Finally, use it as follows:
>
> ```shell
> $ gpg -d -q .sshpasswd.gpg | sshpass ssh user@srv1.example.com
> ```

我们来测试一下。





参考：

- [How to Use ssh-keygen to Generate a New SSH Key](https://www.ssh.com/academy/ssh/keygen)
- [How to Add a Comment to an existing SSH Public Key](https://nixcp.com/add-comment-to-existing-ssh-public-key/)
- [Test if SSH private key has password protection](https://unix.stackexchange.com/questions/374109/test-if-ssh-private-key-has-password-protection)
- [SSH password automation in Linux with sshpass](https://www.redhat.com/sysadmin/ssh-automation-sshpass)
- [ssh-keygen 生成密钥](https://gnu-linux.readthedocs.io/zh/latest/Chapter01/00_ssh-keygen.html)
- 
