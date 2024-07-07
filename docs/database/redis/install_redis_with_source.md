# CentOS7源码安装Redis6.2.14

[[toc]]

## 1. 下载并校验文件散列值

在这个页面 [https://github.com/redis/redis-hashes/](https://github.com/redis/redis-hashes/) 可以看到redis各版本版本对应的散列值：

```sh
hash redis-6.2.14.tar.gz sha256 34e74856cbd66fdb3a684fb349d93961d8c7aa668b06f81fd93ff267d09bc277 http://download.redis.io/releases/redis-6.2.14.tar.gz
```



从 https://redis.io/downloads/ 或 [https://download.redis.io/releases/redis-6.2.14.tar.gz](https://download.redis.io/releases/redis-6.2.14.tar.gz) 下载Redis源码文件。

然后上传到远程主机上。

```sh
# 远程主机操作系统信息
[root@redis-server ~]# cat /etc/centos-release
CentOS Linux release 7.9.2009 (Core)
```



校验sha256值：

```sh
[root@redis-server ~]# ls -lah redis-6.2.14.tar.gz
-rw-r--r-- 1 root root 2.4M Jun 10 17:23 redis-6.2.14.tar.gz
[root@redis-server ~]# sha256sum redis-6.2.14.tar.gz |grep 34e74856cbd66fdb3a684fb349d93961d8c7aa668b06f81fd93ff267d09bc277
34e74856cbd66fdb3a684fb349d93961d8c7aa668b06f81fd93ff267d09bc277  redis-6.2.14.tar.gz
[root@redis-server ~]#
```

可以看到sha256散列值校验正常。



## 2. 解压

```sh
[root@redis-server ~]# tar -zxvf redis-6.2.14.tar.gz
redis-6.2.14/
redis-6.2.14/.github/
redis-6.2.14/.github/ISSUE_TEMPLATE/
redis-6.2.14/.github/ISSUE_TEMPLATE/bug_report.md
redis-6.2.14/.github/ISSUE_TEMPLATE/crash_report.md
redis-6.2.14/.github/ISSUE_TEMPLATE/feature_request.md
redis-6.2.14/.github/ISSUE_TEMPLATE/other_stuff.md
redis-6.2.14/.github/ISSUE_TEMPLATE/question.md
redis-6.2.14/.github/workflows/
redis-6.2.14/.github/workflows/ci.yml
redis-6.2.14/.github/workflows/daily.yml
redis-6.2.14/.gitignore
redis-6.2.14/00-RELEASENOTES
redis-6.2.14/BUGS
redis-6.2.14/CONDUCT
redis-6.2.14/CONTRIBUTING
redis-6.2.14/COPYING
redis-6.2.14/INSTALL
redis-6.2.14/MANIFESTO
redis-6.2.14/Makefile
redis-6.2.14/README.md
redis-6.2.14/TLS.md
redis-6.2.14/deps/
redis-6.2.14/deps/Makefile
redis-6.2.14/deps/README.md
... 省略
redis-6.2.14/utils/install_server.sh
redis-6.2.14/utils/lru/
redis-6.2.14/utils/lru/README
redis-6.2.14/utils/lru/lfu-simulation.c
redis-6.2.14/utils/lru/test-lru.rb
redis-6.2.14/utils/redis-copy.rb
redis-6.2.14/utils/redis-sha1.rb
redis-6.2.14/utils/redis_init_script
redis-6.2.14/utils/redis_init_script.tpl
redis-6.2.14/utils/releasetools/
redis-6.2.14/utils/releasetools/01_create_tarball.sh
redis-6.2.14/utils/releasetools/02_upload_tarball.sh
redis-6.2.14/utils/releasetools/03_test_release.sh
redis-6.2.14/utils/releasetools/04_release_hash.sh
redis-6.2.14/utils/releasetools/changelog.tcl
redis-6.2.14/utils/speed-regression.tcl
redis-6.2.14/utils/srandmember/
redis-6.2.14/utils/srandmember/README.md
redis-6.2.14/utils/srandmember/showdist.rb
redis-6.2.14/utils/srandmember/showfreq.rb
redis-6.2.14/utils/systemd-redis_multiple_servers@.service
redis-6.2.14/utils/systemd-redis_server.service
redis-6.2.14/utils/tracking_collisions.c
redis-6.2.14/utils/whatisdoing.sh
[root@redis-server ~]# echo $?
0
[root@redis-server ~]#
```

解压成功。

## 3. 编译

编译前，需要确保系统已经正常安装`gcc`包。

```sh
[root@redis-server ~]# rpm -qa|grep gcc
libgcc-4.8.5-44.el7.x86_64
gcc-4.8.5-44.el7.x86_64
[root@redis-server ~]#
```

如果没有的话，使用`yum install -y gcc`安装一下。

切换到`redis-6.2.14`目录：

```sh
[root@redis-server ~]# cd redis-6.2.14
[root@redis-server redis-6.2.14]# ls
00-RELEASENOTES  BUGS  CONDUCT  CONTRIBUTING  COPYING  deps  INSTALL  Makefile  MANIFESTO  README.md  redis.conf  runtest  runtest-cluster  runtest-moduleapi  runtest-sentinel  sentinel.conf  src  tests  TLS.md  utils
[root@redis-server redis-6.2.14]#
```

使用`make`命令编译：

```sh
[root@redis-server redis-6.2.14]# make
cd src && make all
make[1]: Entering directory `/root/redis-6.2.14/src'
    CC Makefile.dep
make[1]: Leaving directory `/root/redis-6.2.14/src'
make[1]: Entering directory `/root/redis-6.2.14/src'
rm -rf redis-server redis-sentinel redis-cli redis-benchmark redis-check-rdb redis-check-aof *.o *.gcda *.gcno *.gcov redis.info lcov-html Makefile.dep
rm -f adlist.d quicklist.d ae.d anet.d dict.d server.d sds.d zmalloc.d lzf_c.d lzf_d.d pqsort.d zipmap.d sha1.d ziplist.d release.d networking.d util.d object.d db.d replication.d rdb.d t_string.d t_list.d t_set.d t_zset.d t_hash.d config.d aof.d pubsub.d multi.d debug.d sort.d intset.d syncio.d cluster.d crc16.d endianconv.d slowlog.d scripting.d bio.d rio.d rand.d memtest.d crcspeed.d crc64.d bitops.d sentinel.d notify.d setproctitle.d blocked.d hyperloglog.d latency.d sparkline.d redis-check-rdb.d redis-check-aof.d geo.d lazyfree.d module.d evict.d expire.d geohash.d geohash_helper.d childinfo.d defrag.d siphash.d rax.d t_stream.d listpack.d localtime.d lolwut.d lolwut5.d lolwut6.d acl.d gopher.d tracking.d connection.d tls.d sha256.d timeout.d setcpuaffinity.d monotonic.d mt19937-64.d anet.d adlist.d dict.d redis-cli.d zmalloc.d release.d ae.d crcspeed.d crc64.d siphash.d crc16.d monotonic.d cli_common.d mt19937-64.d ae.d anet.d redis-benchmark.d adlist.d dict.d zmalloc.d release.d crcspeed.d crc64.d siphash.d crc16.d monotonic.d cli_common.d mt19937-64.d
(cd ../deps && make distclean)
make[2]: Entering directory `/root/redis-6.2.14/deps'
(cd hiredis && make clean) > /dev/null || true
(cd linenoise && make clean) > /dev/null || true
(cd lua && make clean) > /dev/null || true
(cd jemalloc && [ -f Makefile ] && make distclean) > /dev/null || true
(cd hdr_histogram && make clean) > /dev/null || true
(rm -f .make-*)
make[2]: Leaving directory `/root/redis-6.2.14/deps'
(cd modules && make clean)
make[2]: Entering directory `/root/redis-6.2.14/src/modules'
rm -rf *.xo *.so
make[2]: Leaving directory `/root/redis-6.2.14/src/modules'
(cd ../tests/modules && make clean)
make[2]: Entering directory `/root/redis-6.2.14/tests/modules'
rm -f commandfilter.so basics.so testrdb.so fork.so infotest.so propagate.so misc.so hooks.so blockonkeys.so blockonbackground.so scan.so datatype.so auth.so keyspace_events.so blockedclient.so getkeys.so test_lazyfree.so timer.so defragtest.so hash.so zset.so stream.so commandfilter.xo basics.xo testrdb.xo fork.xo infotest.xo propagate.xo misc.xo hooks.xo blockonkeys.xo blockonbackground.xo scan.xo datatype.xo auth.xo keyspace_events.xo blockedclient.xo getkeys.xo test_lazyfree.xo timer.xo defragtest.xo hash.xo zset.xo stream.xo
make[2]: Leaving directory `/root/redis-6.2.14/tests/modules'
(rm -f .make-*)
echo STD=-pedantic -DREDIS_STATIC='' -std=c99 >> .make-settings
echo WARN=-Wall -W -Wno-missing-field-initializers >> .make-settings
echo OPT=-O2 >> .make-settings
echo MALLOC=jemalloc >> .make-settings
echo BUILD_TLS= >> .make-settings
echo USE_SYSTEMD= >> .make-settings
echo CFLAGS= >> .make-settings
echo LDFLAGS= >> .make-settings
echo REDIS_CFLAGS= >> .make-settings
echo REDIS_LDFLAGS= >> .make-settings
echo PREV_FINAL_CFLAGS=-pedantic -DREDIS_STATIC='' -std=c99 -Wall -W -Wno-missing-field-initializers -O2 -g -ggdb   -I../deps/hiredis -I../deps/linenoise -I../deps/lua/src -I../deps/hdr_histogram -DUSE_JEMALLOC -I../deps/jemalloc/include >> .make-settings
echo PREV_FINAL_LDFLAGS=  -g -ggdb -rdynamic >> .make-settings
(cd ../deps && make hiredis linenoise lua hdr_histogram jemalloc)
make[2]: Entering directory `/root/redis-6.2.14/deps'
(cd hiredis && make clean) > /dev/null || true
(cd linenoise && make clean) > /dev/null || true
(cd lua && make clean) > /dev/null || true
(cd jemalloc && [ -f Makefile ] && make distclean) > /dev/null || true
(cd hdr_histogram && make clean) > /dev/null || true
(rm -f .make-*)
(echo "" > .make-cflags)
(echo "" > .make-ldflags)
MAKE hiredis
cd hiredis && make static
make[3]: Entering directory `/root/redis-6.2.14/deps/hiredis'
cc -std=c99 -pedantic -c -O3 -fPIC   -Wall -W -Wstrict-prototypes -Wwrite-strings -Wno-missing-field-initializers -g -ggdb alloc.c
cc -std=c99 -pedantic -c -O3 -fPIC   -Wall -W -Wstrict-prototypes -Wwrite-strings -Wno-missing-field-initializers -g -ggdb net.c
cc -std=c99 -pedantic -c -O3 -fPIC   -Wall -W -Wstrict-prototypes -Wwrite-strings -Wno-missing-field-initializers -g -ggdb hiredis.c
cc -std=c99 -pedantic -c -O3 -fPIC   -Wall -W -Wstrict-prototypes -Wwrite-strings -Wno-missing-field-initializers -g -ggdb sds.c
cc -std=c99 -pedantic -c -O3 -fPIC   -Wall -W -Wstrict-prototypes -Wwrite-strings -Wno-missing-field-initializers -g -ggdb async.c
cc -std=c99 -pedantic -c -O3 -fPIC   -Wall -W -Wstrict-prototypes -Wwrite-strings -Wno-missing-field-initializers -g -ggdb read.c
cc -std=c99 -pedantic -c -O3 -fPIC   -Wall -W -Wstrict-prototypes -Wwrite-strings -Wno-missing-field-initializers -g -ggdb sockcompat.c
ar rcs libhiredis.a alloc.o net.o hiredis.o sds.o async.o read.o sockcompat.o
make[3]: Leaving directory `/root/redis-6.2.14/deps/hiredis'
MAKE linenoise
cd linenoise && make
make[3]: Entering directory `/root/redis-6.2.14/deps/linenoise'
cc  -Wall -Os -g  -c linenoise.c
make[3]: Leaving directory `/root/redis-6.2.14/deps/linenoise'
MAKE lua
cd lua/src && make all CFLAGS="-O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP " MYLDFLAGS="" AR="ar rc"
make[3]: Entering directory `/root/redis-6.2.14/deps/lua/src'
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lapi.o lapi.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lcode.o lcode.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o ldebug.o ldebug.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o ldo.o ldo.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o ldump.o ldump.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lfunc.o lfunc.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lgc.o lgc.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o llex.o llex.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lmem.o lmem.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lobject.o lobject.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lopcodes.o lopcodes.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lparser.o lparser.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lstate.o lstate.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lstring.o lstring.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o ltable.o ltable.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o ltm.o ltm.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lundump.o lundump.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lvm.o lvm.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lzio.o lzio.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o strbuf.o strbuf.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o fpconv.o fpconv.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lauxlib.o lauxlib.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lbaselib.o lbaselib.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o ldblib.o ldblib.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o liolib.o liolib.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lmathlib.o lmathlib.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o loslib.o loslib.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o ltablib.o ltablib.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lstrlib.o lstrlib.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o loadlib.o loadlib.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o linit.o linit.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lua_cjson.o lua_cjson.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lua_struct.o lua_struct.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lua_cmsgpack.o lua_cmsgpack.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lua_bit.o lua_bit.c
ar rc liblua.a lapi.o lcode.o ldebug.o ldo.o ldump.o lfunc.o lgc.o llex.o lmem.o lobject.o lopcodes.o lparser.o lstate.o lstring.o ltable.o ltm.o lundump.o lvm.o lzio.o strbuf.o fpconv.o lauxlib.o lbaselib.o ldblib.o liolib.o lmathlib.o loslib.o ltablib.o lstrlib.o loadlib.o linit.o lua_cjson.o lua_struct.o lua_cmsgpack.o lua_bit.o # DLL needs all object files
ranlib liblua.a
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o lua.o lua.c
cc -o lua  lua.o liblua.a -lm
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o luac.o luac.c
cc -O2 -Wall -DLUA_ANSI -DENABLE_CJSON_GLOBAL -DREDIS_STATIC='' -DLUA_USE_MKSTEMP    -c -o print.o print.c
cc -o luac  luac.o print.o liblua.a -lm
make[3]: Leaving directory `/root/redis-6.2.14/deps/lua/src'
MAKE hdr_histogram
cd hdr_histogram && make
make[3]: Entering directory `/root/redis-6.2.14/deps/hdr_histogram'
cc  -Wall -Os -g  -c  hdr_histogram.c
make[3]: Leaving directory `/root/redis-6.2.14/deps/hdr_histogram'
MAKE jemalloc
cd jemalloc && ./configure --with-version=5.1.0-0-g0 --with-lg-quantum=3 --with-jemalloc-prefix=je_ CFLAGS="-std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops " LDFLAGS=""
checking for xsltproc... /usr/bin/xsltproc
checking for gcc... gcc
checking whether the C compiler works... yes
checking for C compiler default output file name... a.out
checking for suffix of executables...
checking whether we are cross compiling... no
checking for suffix of object files... o
checking whether we are using the GNU C compiler... yes
checking whether gcc accepts -g... yes
checking for gcc option to accept ISO C89... none needed
checking whether compiler is cray... no
checking whether compiler supports -std=gnu11... yes
checking whether compiler supports -Wall... yes
checking whether compiler supports -Wshorten-64-to-32... no
checking whether compiler supports -Wsign-compare... yes
checking whether compiler supports -Wundef... yes
checking whether compiler supports -Wno-format-zero-length... yes
checking whether compiler supports -pipe... yes
checking whether compiler supports -g3... yes
checking how to run the C preprocessor... gcc -E
checking for g++... no
checking for c++... no
checking for gpp... no
checking for aCC... no
checking for CC... no
checking for cxx... no
checking for cc++... no
checking for cl.exe... no
checking for FCC... no
checking for KCC... no
checking for RCC... no
checking for xlC_r... no
checking for xlC... no
checking whether we are using the GNU C++ compiler... no
checking whether g++ accepts -g... no
checking whether g++ supports C++14 features by default... no
checking whether g++ supports C++14 features with -std=c++14... no
checking whether g++ supports C++14 features with -std=c++0x... no
checking whether g++ supports C++14 features with +std=c++14... no
checking whether g++ supports C++14 features with -h std=c++14... no
configure: No compiler with C++14 support was found
checking for grep that handles long lines and -e... /usr/bin/grep
checking for egrep... /usr/bin/grep -E
checking for ANSI C header files... yes
checking for sys/types.h... yes
checking for sys/stat.h... yes
checking for stdlib.h... yes
checking for string.h... yes
checking for memory.h... yes
checking for strings.h... yes
checking for inttypes.h... yes
checking for stdint.h... yes
checking for unistd.h... yes
checking whether byte ordering is bigendian... no
checking size of void *... 8
checking size of int... 4
checking size of long... 8
checking size of long long... 8
checking size of intmax_t... 8
checking build system type... x86_64-pc-linux-gnu
checking host system type... x86_64-pc-linux-gnu
checking whether pause instruction is compilable... yes
checking number of significant virtual address bits... 48
checking for ar... ar
checking for nm... nm
checking for gawk... gawk
checking malloc.h usability... yes
checking malloc.h presence... yes
checking for malloc.h... yes
checking whether malloc_usable_size definition can use const argument... no
checking for library containing log... -lm
checking whether __attribute__ syntax is compilable... yes
checking whether compiler supports -fvisibility=hidden... yes
checking whether compiler supports -fvisibility=hidden... no
checking whether compiler supports -Werror... yes
checking whether compiler supports -herror_on_warning... no
checking whether tls_model attribute is compilable... yes
checking whether compiler supports -Werror... yes
checking whether compiler supports -herror_on_warning... no
checking whether alloc_size attribute is compilable... yes
checking whether compiler supports -Werror... yes
checking whether compiler supports -herror_on_warning... no
checking whether format(gnu_printf, ...) attribute is compilable... yes
checking whether compiler supports -Werror... yes
checking whether compiler supports -herror_on_warning... no
checking whether format(printf, ...) attribute is compilable... yes
checking for a BSD-compatible install... /usr/bin/install -c
checking for ranlib... ranlib
checking for ld... /usr/bin/ld
checking for autoconf... false
checking for memalign... yes
checking for valloc... yes
checking whether compiler supports -O3... yes
checking whether compiler supports -O3... no
checking whether compiler supports -funroll-loops... yes
checking configured backtracing method... N/A
checking for sbrk... yes
checking whether utrace(2) is compilable... no
checking whether a program using __builtin_unreachable is compilable... yes
checking whether a program using __builtin_ffsl is compilable... yes
checking LG_PAGE... 12
checking pthread.h usability... yes
checking pthread.h presence... yes
checking for pthread.h... yes
checking for pthread_create in -lpthread... yes
checking dlfcn.h usability... yes
checking dlfcn.h presence... yes
checking for dlfcn.h... yes
checking for dlsym... no
checking for dlsym in -ldl... yes
checking whether pthread_atfork(3) is compilable... yes
checking whether pthread_setname_np(3) is compilable... yes
checking for library containing clock_gettime... none required
checking whether clock_gettime(CLOCK_MONOTONIC_COARSE, ...) is compilable... yes
checking whether clock_gettime(CLOCK_MONOTONIC, ...) is compilable... yes
checking whether mach_absolute_time() is compilable... no
checking whether compiler supports -Werror... yes
checking whether syscall(2) is compilable... yes
checking for secure_getenv... yes
checking for sched_getcpu... yes
checking for sched_setaffinity... yes
checking for issetugid... no
checking for _malloc_thread_cleanup... no
checking for _pthread_mutex_init_calloc_cb... no
checking for TLS... yes
checking whether C11 atomics is compilable... no
checking whether GCC __atomic atomics is compilable... yes
checking whether GCC __sync atomics is compilable... yes
checking whether Darwin OSAtomic*() is compilable... no
checking whether madvise(2) is compilable... yes
checking whether madvise(..., MADV_FREE) is compilable... no
checking whether madvise(..., MADV_DONTNEED) is compilable... yes
checking whether madvise(..., MADV_DO[NT]DUMP) is compilable... yes
checking whether madvise(..., MADV_[NO]HUGEPAGE) is compilable... yes
checking whether to force 32-bit __sync_{add,sub}_and_fetch()... no
checking whether to force 64-bit __sync_{add,sub}_and_fetch()... no
checking for __builtin_clz... yes
checking whether Darwin os_unfair_lock_*() is compilable... no
checking whether Darwin OSSpin*() is compilable... no
checking whether glibc malloc hook is compilable... yes
checking whether glibc memalign hook is compilable... yes
checking whether pthreads adaptive mutexes is compilable... yes
checking whether compiler supports -D_GNU_SOURCE... yes
checking whether compiler supports -Werror... yes
checking whether compiler supports -herror_on_warning... no
checking whether strerror_r returns char with gnu source is compilable... yes
checking for stdbool.h that conforms to C99... yes
checking for _Bool... yes
configure: creating ./config.status
config.status: creating Makefile
config.status: creating jemalloc.pc
config.status: creating doc/html.xsl
config.status: creating doc/manpages.xsl
config.status: creating doc/jemalloc.xml
config.status: creating include/jemalloc/jemalloc_macros.h
config.status: creating include/jemalloc/jemalloc_protos.h
config.status: creating include/jemalloc/jemalloc_typedefs.h
config.status: creating include/jemalloc/internal/jemalloc_preamble.h
config.status: creating test/test.sh
config.status: creating test/include/test/jemalloc_test.h
config.status: creating config.stamp
config.status: creating bin/jemalloc-config
config.status: creating bin/jemalloc.sh
config.status: creating bin/jeprof
config.status: creating include/jemalloc/jemalloc_defs.h
config.status: creating include/jemalloc/internal/jemalloc_internal_defs.h
config.status: creating test/include/test/jemalloc_test_defs.h
config.status: executing include/jemalloc/internal/public_symbols.txt commands
config.status: executing include/jemalloc/internal/private_symbols.awk commands
config.status: executing include/jemalloc/internal/private_symbols_jet.awk commands
config.status: executing include/jemalloc/internal/public_namespace.h commands
config.status: executing include/jemalloc/internal/public_unnamespace.h commands
config.status: executing include/jemalloc/internal/size_classes.h commands
config.status: executing include/jemalloc/jemalloc_protos_jet.h commands
config.status: executing include/jemalloc/jemalloc_rename.h commands
config.status: executing include/jemalloc/jemalloc_mangle.h commands
config.status: executing include/jemalloc/jemalloc_mangle_jet.h commands
config.status: executing include/jemalloc/jemalloc.h commands
===============================================================================
jemalloc version   : 5.1.0-0-g0
library revision   : 2

CONFIG             : --with-version=5.1.0-0-g0 --with-lg-quantum=3 --with-jemalloc-prefix=je_ 'CFLAGS=-std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops ' LDFLAGS=
CC                 : gcc
CONFIGURE_CFLAGS   : -std=gnu11 -Wall -Wsign-compare -Wundef -Wno-format-zero-length -pipe -g3 -fvisibility=hidden -O3 -funroll-loops
SPECIFIED_CFLAGS   : -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops
EXTRA_CFLAGS       :
CPPFLAGS           : -D_GNU_SOURCE -D_REENTRANT
CXX                : g++
CONFIGURE_CXXFLAGS :
SPECIFIED_CXXFLAGS :
EXTRA_CXXFLAGS     :
LDFLAGS            :
EXTRA_LDFLAGS      :
DSO_LDFLAGS        : -shared -Wl,-soname,$(@F)
LIBS               : -lm  -lpthread -ldl
RPATH_EXTRA        :

XSLTPROC           : /usr/bin/xsltproc
XSLROOT            :

PREFIX             : /usr/local
BINDIR             : /usr/local/bin
DATADIR            : /usr/local/share
INCLUDEDIR         : /usr/local/include
LIBDIR             : /usr/local/lib
MANDIR             : /usr/local/share/man

srcroot            :
abs_srcroot        : /root/redis-6.2.14/deps/jemalloc/
objroot            :
abs_objroot        : /root/redis-6.2.14/deps/jemalloc/

JEMALLOC_PREFIX    : je_
JEMALLOC_PRIVATE_NAMESPACE
                   : je_
install_suffix     :
malloc_conf        :
autogen            : 0
debug              : 0
stats              : 1
prof               : 0
prof-libunwind     : 0
prof-libgcc        : 0
prof-gcc           : 0
fill               : 1
utrace             : 0
xmalloc            : 0
log                : 0
lazy_lock          : 0
cache-oblivious    : 1
cxx                : 0
===============================================================================
cd jemalloc && make CFLAGS="-std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops " LDFLAGS="" lib/libjemalloc.a
make[3]: Entering directory `/root/redis-6.2.14/deps/jemalloc'
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/jemalloc.sym.o src/jemalloc.c
nm -a src/jemalloc.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/jemalloc.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/arena.sym.o src/arena.c
nm -a src/arena.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/arena.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/background_thread.sym.o src/background_thread.c
nm -a src/background_thread.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/background_thread.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/base.sym.o src/base.c
nm -a src/base.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/base.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/bin.sym.o src/bin.c
nm -a src/bin.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/bin.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/bitmap.sym.o src/bitmap.c
nm -a src/bitmap.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/bitmap.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/ckh.sym.o src/ckh.c
nm -a src/ckh.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/ckh.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/ctl.sym.o src/ctl.c
nm -a src/ctl.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/ctl.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/div.sym.o src/div.c
nm -a src/div.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/div.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/extent.sym.o src/extent.c
nm -a src/extent.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/extent.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/extent_dss.sym.o src/extent_dss.c
nm -a src/extent_dss.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/extent_dss.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/extent_mmap.sym.o src/extent_mmap.c
nm -a src/extent_mmap.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/extent_mmap.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/hash.sym.o src/hash.c
nm -a src/hash.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/hash.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/hooks.sym.o src/hooks.c
nm -a src/hooks.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/hooks.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/large.sym.o src/large.c
nm -a src/large.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/large.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/log.sym.o src/log.c
nm -a src/log.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/log.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/malloc_io.sym.o src/malloc_io.c
nm -a src/malloc_io.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/malloc_io.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/mutex.sym.o src/mutex.c
nm -a src/mutex.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/mutex.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/mutex_pool.sym.o src/mutex_pool.c
nm -a src/mutex_pool.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/mutex_pool.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/nstime.sym.o src/nstime.c
nm -a src/nstime.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/nstime.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/pages.sym.o src/pages.c
nm -a src/pages.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/pages.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/prng.sym.o src/prng.c
nm -a src/prng.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/prng.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/prof.sym.o src/prof.c
nm -a src/prof.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/prof.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/rtree.sym.o src/rtree.c
nm -a src/rtree.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/rtree.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/stats.sym.o src/stats.c
nm -a src/stats.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/stats.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/sz.sym.o src/sz.c
nm -a src/sz.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/sz.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/tcache.sym.o src/tcache.c
nm -a src/tcache.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/tcache.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/ticker.sym.o src/ticker.c
nm -a src/ticker.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/ticker.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/tsd.sym.o src/tsd.c
nm -a src/tsd.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/tsd.sym
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -DJEMALLOC_NO_PRIVATE_NAMESPACE -o src/witness.sym.o src/witness.c
nm -a src/witness.sym.o | gawk -f include/jemalloc/internal/private_symbols.awk > src/witness.sym
/bin/sh include/jemalloc/internal/private_namespace.sh src/jemalloc.sym src/arena.sym src/background_thread.sym src/base.sym src/bin.sym src/bitmap.sym src/ckh.sym src/ctl.sym src/div.sym src/extent.sym src/extent_dss.sym src/extent_mmap.sym src/hash.sym src/hooks.sym src/large.sym src/log.sym src/malloc_io.sym src/mutex.sym src/mutex_pool.sym src/nstime.sym src/pages.sym src/prng.sym src/prof.sym src/rtree.sym src/stats.sym src/sz.sym src/tcache.sym src/ticker.sym src/tsd.sym src/witness.sym > include/jemalloc/internal/private_namespace.gen.h
cp include/jemalloc/internal/private_namespace.gen.h include/jemalloc/internal/private_namespace.gen.h
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/jemalloc.o src/jemalloc.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/arena.o src/arena.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/background_thread.o src/background_thread.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/base.o src/base.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/bin.o src/bin.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/bitmap.o src/bitmap.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/ckh.o src/ckh.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/ctl.o src/ctl.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/div.o src/div.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/extent.o src/extent.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/extent_dss.o src/extent_dss.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/extent_mmap.o src/extent_mmap.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/hash.o src/hash.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/hooks.o src/hooks.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/large.o src/large.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/log.o src/log.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/malloc_io.o src/malloc_io.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/mutex.o src/mutex.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/mutex_pool.o src/mutex_pool.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/nstime.o src/nstime.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/pages.o src/pages.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/prng.o src/prng.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/prof.o src/prof.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/rtree.o src/rtree.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/stats.o src/stats.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/sz.o src/sz.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/tcache.o src/tcache.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/ticker.o src/ticker.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/tsd.o src/tsd.c
gcc -std=gnu99 -Wall -pipe -g3 -O3 -funroll-loops  -c -D_GNU_SOURCE -D_REENTRANT -Iinclude -Iinclude -o src/witness.o src/witness.c
ar crus lib/libjemalloc.a src/jemalloc.o src/arena.o src/background_thread.o src/base.o src/bin.o src/bitmap.o src/ckh.o src/ctl.o src/div.o src/extent.o src/extent_dss.o src/extent_mmap.o src/hash.o src/hooks.o src/large.o src/log.o src/malloc_io.o src/mutex.o src/mutex_pool.o src/nstime.o src/pages.o src/prng.o src/prof.o src/rtree.o src/stats.o src/sz.o src/tcache.o src/ticker.o src/tsd.o src/witness.o
make[3]: Leaving directory `/root/redis-6.2.14/deps/jemalloc'
make[2]: Leaving directory `/root/redis-6.2.14/deps'
    CC adlist.o
    CC quicklist.o
    CC ae.o
    CC anet.o
    CC dict.o
    CC server.o
    CC sds.o
    CC zmalloc.o
    CC lzf_c.o
    CC lzf_d.o
    CC pqsort.o
    CC zipmap.o
    CC sha1.o
    CC ziplist.o
    CC release.o
    CC networking.o
    CC util.o
    CC object.o
    CC db.o
    CC replication.o
    CC rdb.o
    CC t_string.o
    CC t_list.o
    CC t_set.o
    CC t_zset.o
    CC t_hash.o
    CC config.o
    CC aof.o
    CC pubsub.o
    CC multi.o
    CC debug.o
    CC sort.o
    CC intset.o
    CC syncio.o
    CC cluster.o
    CC crc16.o
    CC endianconv.o
    CC slowlog.o
    CC scripting.o
    CC bio.o
    CC rio.o
    CC rand.o
    CC memtest.o
    CC crcspeed.o
    CC crc64.o
    CC bitops.o
    CC sentinel.o
    CC notify.o
    CC setproctitle.o
    CC blocked.o
    CC hyperloglog.o
    CC latency.o
    CC sparkline.o
    CC redis-check-rdb.o
    CC redis-check-aof.o
    CC geo.o
    CC lazyfree.o
    CC module.o
    CC evict.o
    CC expire.o
    CC geohash.o
    CC geohash_helper.o
    CC childinfo.o
    CC defrag.o
    CC siphash.o
    CC rax.o
    CC t_stream.o
    CC listpack.o
    CC localtime.o
    CC lolwut.o
    CC lolwut5.o
    CC lolwut6.o
    CC acl.o
    CC gopher.o
    CC tracking.o
    CC connection.o
    CC tls.o
    CC sha256.o
    CC timeout.o
    CC setcpuaffinity.o
    CC monotonic.o
    CC mt19937-64.o
    LINK redis-server
    INSTALL redis-sentinel
    CC redis-cli.o
    CC cli_common.o
    LINK redis-cli
    CC redis-benchmark.o
    LINK redis-benchmark
    INSTALL redis-check-rdb
    INSTALL redis-check-aof

Hint: It's a good idea to run 'make test' ;)

make[1]: Leaving directory `/root/redis-6.2.14/src'
[root@redis-server redis-6.2.14]#
```

可以看到出现了`It's a good idea to run 'make test'`提示，表示编译成功。

## 4. 安装

使用`make install PREFIX=/srv/redis-6.2.14`命令安装，安装时指定安装目录。

```sh
[root@redis-server redis-6.2.14]# make install PREFIX=/srv/redis-6.2.14
cd src && make install
make[1]: Entering directory `/root/redis-6.2.14/src'
    CC Makefile.dep
make[1]: Leaving directory `/root/redis-6.2.14/src'
make[1]: Entering directory `/root/redis-6.2.14/src'

Hint: It's a good idea to run 'make test' ;)

    INSTALL redis-server
    INSTALL redis-benchmark
    INSTALL redis-cli
make[1]: Leaving directory `/root/redis-6.2.14/src'
[root@redis-server redis-6.2.14]# echo $?
0
[root@redis-server redis-6.2.14]# ll /srv/redis-6.2.14
total 0
drwxr-xr-x 2 root root 134 Jun 10 18:25 bin
[root@redis-server redis-6.2.14]# ll /srv/redis-6.2.14/bin/
total 18936
-rwxr-xr-x 1 root root 4830616 Jun 10 18:25 redis-benchmark
lrwxrwxrwx 1 root root      12 Jun 10 18:25 redis-check-aof -> redis-server
lrwxrwxrwx 1 root root      12 Jun 10 18:25 redis-check-rdb -> redis-server
-rwxr-xr-x 1 root root 5004728 Jun 10 18:25 redis-cli
lrwxrwxrwx 1 root root      12 Jun 10 18:25 redis-sentinel -> redis-server
-rwxr-xr-x 1 root root 9548176 Jun 10 18:25 redis-server
[root@redis-server redis-6.2.14]#
```

可以看到，安装成功，并生成了相应对应的二进制文件。



## 5. 校验

查看`redis-server`和`redis-cli`的版本信息：

```sh
[root@redis-server redis-6.2.14]# cd /srv/redis-6.2.14/bin/
[root@redis-server bin]# ./redis-server --version
Redis server v=6.2.14 sha=00000000:0 malloc=jemalloc-5.1.0 bits=64 build=ad623970888ef0a
[root@redis-server bin]# ./redis-cli --version
redis-cli 6.2.14
[root@redis-server bin]#
```

可以看到，能够正常显示`redis-server`和`redis-cli`的版本信息。



## 6. 复制redis配置文件

在redis源码中配置有一个配置文件，我们将它复制到`/srv/redis-6.2.14/conf`目录下。

```sh
[root@redis-server ~]# ls -lah redis-6.2.14/redis.conf
-rw-rw-r-- 1 root root 92K Oct 18  2023 redis-6.2.14/redis.conf
[root@redis-server ~]# cd /srv/redis-6.2.14
[root@redis-server redis-6.2.14]# mkdir conf
[root@redis-server redis-6.2.14]# cp -p ~/redis-6.2.14/redis.conf conf
[root@redis-server redis-6.2.14]# ls -lah conf/redis.conf
-rw-rw-r-- 1 root root 92K Oct 18  2023 conf/redis.conf
[root@redis-server redis-6.2.14]#
```

保存一份默认的配置文件：

```sh
[root@redis-server redis-6.2.14]# cp -p conf/redis.conf conf/redis.conf.default
[root@redis-server redis-6.2.14]# md5sum conf/*
d9a1e1fba487325b188ee5ec7bd78ae5  conf/redis.conf
d9a1e1fba487325b188ee5ec7bd78ae5  conf/redis.conf.default
[root@redis-server redis-6.2.14]#
```



## 7. 修改redis配置文件

修改redis配置，最后查看未注释的配置：

```sh
[root@redis-server redis-6.2.14]# grep -v '#' conf/redis.conf|awk NF
bind 192.168.56.121 127.0.0.1
protected-mode no
port 29736
tcp-backlog 511
timeout 300
tcp-keepalive 300
daemonize no
pidfile /srv/redis/pid/redis_29736.pid
loglevel notice
logfile "/srv/redis/logs/redis_29736.log"
crash-log-enabled yes
databases 16
always-show-logo no
set-proc-title no
proc-title-template "{title} {listen-addr} {server-mode}"
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
rdb-del-sync-files no
dir /srv/redis/data
replica-serve-stale-data yes
replica-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-diskless-load disabled
repl-disable-tcp-nodelay no
replica-priority 100
acllog-max-len 128
requirepass ALONGPASSWORD
maxmemory 1gb
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
replica-lazy-flush no
lazyfree-lazy-user-del no
lazyfree-lazy-user-flush no
oom-score-adj no
oom-score-adj-values 0 200 800
disable-thp yes
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
aof-use-rdb-preamble yes
lua-time-limit 5000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
stream-node-max-bytes 4096
stream-node-max-entries 100
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
dynamic-hz yes
aof-rewrite-incremental-fsync yes
rdb-save-incremental-fsync yes
jemalloc-bg-thread yes
[root@redis-server redis-6.2.14]#
```

创建相关目录：

```sh
[root@redis-server redis-6.2.14]# cd /srv/
[root@redis-server srv]# ln -s redis-6.2.14 redis
[root@redis-server srv]# mkdir redis/{pid,logs,data}
[root@redis-server srv]# ls -d redis/{pid,logs,data}
redis/data  redis/logs  redis/pid
```

## 8. 启动redis服务

### 8.1 尝试启动redis服务

```sh
[root@redis-server ~]# cd /srv/
[root@redis-server redis]# ./bin/redis-server ./conf/redis.conf
```

此时，redis服务是在前台启动的。我们重新开一个控制台窗口，查看redis服务状态。

```sh
[root@redis-server ~]# ps -ef|grep redis
root      1820  1479  0 11:35 pts/0    00:00:00 ./bin/redis-server ./conf/redis.conf
root      2567  1532  0 11:49 pts/1    00:00:00 grep --color=always redis
[root@redis-server ~]# netstat -tunlp|grep redis
tcp        0      0 127.0.0.1:29736         0.0.0.0:*               LISTEN      1820/./bin/redis-se
tcp        0      0 192.168.56.121:29736    0.0.0.0:*               LISTEN      1820/./bin/redis-se
[root@redis-server ~]#
```

可以看到，服务启动了。查看一下日志:

```sh
[root@redis-server ~]# tail /srv/redis/logs/redis_29736.log
1820:C 07 Jul 2024 11:35:09.760 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
1820:C 07 Jul 2024 11:35:09.760 # Redis version=6.2.14, bits=64, commit=00000000, modified=0, pid=1820, just started
1820:C 07 Jul 2024 11:35:09.760 # Configuration loaded
1820:M 07 Jul 2024 11:35:09.760 * Increased maximum number of open files to 10032 (it was originally set to 1024).
1820:M 07 Jul 2024 11:35:09.760 * monotonic clock: POSIX clock_gettime
1820:M 07 Jul 2024 11:35:09.760 * Running mode=standalone, port=29736.
1820:M 07 Jul 2024 11:35:09.760 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
1820:M 07 Jul 2024 11:35:09.760 # Server initialized
1820:M 07 Jul 2024 11:35:09.760 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
1820:M 07 Jul 2024 11:35:09.760 * Ready to accept connections
[root@redis-server ~]#
```

可以看到，redis日志有了，但其中有两个警告信息。

### 8.2 修复Memory overcommit must be enabled告警

按提示修改`/etc/sysctl.conf `配置文件：

```sh
# 查看当前/etc/sysctl.conf配置
[root@redis-server ~]# cat /etc/sysctl.conf
# sysctl settings are defined through files in
# /usr/lib/sysctl.d/, /run/sysctl.d/, and /etc/sysctl.d/.
#
# Vendors settings live in /usr/lib/sysctl.d/.
# To override a whole file, create a new file with the same in
# /etc/sysctl.d/ and put new settings there. To override
# only specific settings, add a file with a lexically later
# name in /etc/sysctl.d/ and put new settings there.
#
# For more information, see sysctl.conf(5) and sysctl.d(5).


# 修改配置
[root@redis-server ~]# echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf


# 再次查看当前/etc/sysctl.conf配置
[root@redis-server ~]# cat /etc/sysctl.conf
# sysctl settings are defined through files in
# /usr/lib/sysctl.d/, /run/sysctl.d/, and /etc/sysctl.d/.
#
# Vendors settings live in /usr/lib/sysctl.d/.
# To override a whole file, create a new file with the same in
# /etc/sysctl.d/ and put new settings there. To override
# only specific settings, add a file with a lexically later
# name in /etc/sysctl.d/ and put new settings there.
#
# For more information, see sysctl.conf(5) and sysctl.d(5).
vm.overcommit_memory = 1
[root@redis-server ~]# sysctl -p
vm.overcommit_memory = 1
[root@redis-server ~]#

```



再次启动redis服务：

```sh
# 此处是按Ctrl+C停止之前启动的redis服务
[root@redis-server redis]# ./bin/redis-server ./conf/redis.conf^C

# 查看一下sysctl配置生效没有
[root@redis-server redis]# sysctl -p|grep commit
vm.overcommit_memory = 1

# 可以看到配置生效了，清空一下之前的日志
[root@redis-server redis]# > logs/redis_29736.log

# 再次启动服务
[root@redis-server redis]# ./bin/redis-server ./conf/redis.conf
```

此时查看日志已经可以看到没有`WARNING Memory overcommit must be enabled!`告警了：

```sh
[root@redis-server ~]# cat /srv/redis/logs/redis_29736.log
2929:C 07 Jul 2024 11:56:55.391 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
2929:C 07 Jul 2024 11:56:55.391 # Redis version=6.2.14, bits=64, commit=00000000, modified=0, pid=2929, just started
2929:C 07 Jul 2024 11:56:55.391 # Configuration loaded
2929:M 07 Jul 2024 11:56:55.392 * Increased maximum number of open files to 10032 (it was originally set to 1024).
2929:M 07 Jul 2024 11:56:55.392 * monotonic clock: POSIX clock_gettime
2929:M 07 Jul 2024 11:56:55.392 * Running mode=standalone, port=29736.
2929:M 07 Jul 2024 11:56:55.392 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
2929:M 07 Jul 2024 11:56:55.392 # Server initialized
2929:M 07 Jul 2024 11:56:55.392 * Ready to accept connections
[root@redis-server ~]#
```



查看redis相关信息：

```sh
[root@redis-server ~]# /srv/redis/bin/redis-cli -p 29736
127.0.0.1:29736> info memory
NOAUTH Authentication required.
127.0.0.1:29736> auth ALONGPASSWORD
OK
127.0.0.1:29736> info memory
# Memory
used_memory:874208
used_memory_human:853.72K
used_memory_rss:10477568
used_memory_rss_human:9.99M
used_memory_peak:875952
used_memory_peak_human:855.42K
used_memory_peak_perc:99.80%
used_memory_overhead:832632
used_memory_startup:812120
used_memory_dataset:41576
used_memory_dataset_perc:66.96%
allocator_allocated:1180856
allocator_active:1462272
allocator_resident:3829760
total_system_memory:8201236480
total_system_memory_human:7.64G
used_memory_lua:30720
used_memory_lua_human:30.00K
used_memory_scripts:0
used_memory_scripts_human:0B
number_of_cached_scripts:0
maxmemory:1073741824
maxmemory_human:1.00G
maxmemory_policy:noeviction
allocator_frag_ratio:1.24
allocator_frag_bytes:281416
allocator_rss_ratio:2.62
allocator_rss_bytes:2367488
rss_overhead_ratio:2.74
rss_overhead_bytes:6647808
mem_fragmentation_ratio:12.58
mem_fragmentation_bytes:9644376
mem_not_counted_for_evict:4
mem_replication_backlog:0
mem_clients_slaves:0
mem_clients_normal:20504
mem_aof_buffer:8
mem_allocator:jemalloc-5.1.0
active_defrag_running:0
lazyfree_pending_objects:0
lazyfreed_objects:0
127.0.0.1:29736> info replication
# Replication
role:master
connected_slaves:0
master_failover_state:no-failover
master_replid:43d84609e88c12077b3d3e3a3d84dc8a062b9200
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:0
second_repl_offset:-1
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0
127.0.0.1:29736>
```



尝试执行redis基本命令：

```sh
127.0.0.1:29736> set number 6379
OK
127.0.0.1:29736> get number
"6379"
127.0.0.1:29736> set name redis
OK
127.0.0.1:29736> get name
"redis"
127.0.0.1:29736>
```

可以看到，可以正常设置和获取键值。