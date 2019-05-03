from django import forms


class ContainerRunForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Container Name",
        help_text="输入容器名（可选）",
        required=False
    )

    image = forms.CharField(
        max_length=100,
        label="Image",
        help_text="输入镜像名",
        required=True
    )

    internal_port = forms.CharField(
        max_length=20,
        label="Internal Port",
        help_text="输入容器内部服务的端口",
        required=False
    )

    exposed_port = forms.CharField(
        max_length=20,
        label="Exposed Port",
        help_text="暴露映射端口",
        required=False
    )

    network = forms.CharField(
        max_length=100,
        label="Network",
        help_text="输入所属网络",
        required=False
    )

    volumes = forms.CharField(
        max_length=100,
        label="Volumes",
        help_text="输入连接的数据卷",
        required=False
    )

    cmd = forms.CharField(
        max_length=100,
        label="CMD",
        help_text="容器要执行的命令",
        required=False
    )

    autoremove = forms.BooleanField(
        help_text="在容器进程退出后自动删除该容器",
        label="Auto Remove",
        required=False
    )

    autoremove_choices = (
        ('no', 'no'),
        ('always', 'always'),
        ('on-failure', 'on-failure')
    )

    autorestart = forms.ChoiceField(
        choices=autoremove_choices,
        help_text="在容器启动失败后尝试重启",
        label="Auto Restart",
        required=False
    )

    cpu = forms.CharField(
        max_length=10,
        label="CPU Shares",
        help_text="CPU Shares，默认为1024",
        required=False
    )

    mem = forms.CharField(
        max_length=10,
        label="Memory Limit",
        help_text="内存限制，如：100000b, 1000k, 128m, 1g",
        required=False
    )


class ImagePullForm(forms.Form):
    pull_image = forms.CharField(
        max_length=100,
        label="Image",
        help_text="镜像名，若不指定版本则拉取最新的版本",
        required=True
    )


class VolumeCreateForm(forms.Form):
    name = forms.CharField(
        max_length=20,
        label="Volume Name",
        help_text="Volume name",
        required=True
    )

    driver = forms.CharField(
        max_length=20,
        label="Volume Driver",
        help_text="Volume Driver",
        required=False
    )


class NetworkCreateForm(forms.Form):
    scope_choices = (
        ('local', 'local'),
        ('global', 'global'),
        ('swarm', 'swarm'),
    )

    driver_choices = (
        ('host', 'host'),
        ('overlay', 'overlay'),
        ('null', 'null')
    )

    name = forms.CharField(
        max_length=20,
        label="Network Name",
        help_text="网络名",
        required=True
    )

    driver = forms.ChoiceField(
        choices=driver_choices,
        label="Network Driver",
        help_text="网络驱动",
        required=False
    )

    scope = forms.ChoiceField(
        choices=scope_choices,
        label="Network Scope",
        help_text="网络Scope",
        required=False
    )
