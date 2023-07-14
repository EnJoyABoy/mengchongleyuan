var vm = new Vue({
    el: '#app',
	// 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host,
        error_username: false,
        error_password: false,
        error_img_code: false,
        veri_img_code: true,
		error_username_message: '请输入5-20个字符的用户名',
		error_password_message: '请输入8-12位的密码',
        error_image_code_message: '请填写图形验证码',
        username: '',
        password: '',
        image_code_id: '',
        image_code_url: '',
        image_code: '',
        remembered: true
    },
    mounted: function () {
        // 向服务器获取图片验证码
        this.generate_image_code();
    },
    methods: {
        generateUUID: function () {
            var d = new Date().getTime();
            if (window.performance && typeof window.performance.now === "function") {
                d += performance.now(); //use high-precision timer if available
            }
            var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
                var r = (d + Math.random() * 16) % 16 | 0;
                d = Math.floor(d / 16);
                return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
            });
            return uuid;
        },
        // 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
        generate_image_code: function () {
            // 生成一个编号 : 严格一点的使用uuid保证编号唯一， 不是很严谨的情况下，也可以使用时间戳
            this.image_code_id = this.generateUUID();
            // 设置页面中图片验证码img标签的src属性
            this.image_code_url = this.host + "/image_codes/" + this.image_code_id + "/";
            console.log(this.image_code_url);
        },
        // 检查账号
        check_username: function(){
        	var re = /^[a-zA-Z0-9_-]{5,20}$/;
			if (re.test(this.username)) {
                this.error_username = false;
            } else {
                this.error_username = true;
            }
        },
		// 检查密码
        check_pwd: function(){
        	var re = /^[0-9A-Za-z]{8,20}$/;
			if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        // 检查图片验证码，不能为空
        check_image_code: function () {
            var re = /^[0-9A-Za-z]{4}$/;
            if (re.test(this.image_code)) {
                this.error_img_code = false;
                var url = this.host + '/verification_img_code/?image_code=' + this.image_code + '&image_code_id=' + this.image_code_id;
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if(response.data.code == '0'){
                            this.veri_img_code = false;
                        }
                        else{
                            this.veri_img_code = true;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                        this.veri_img_code = true;
                    })
            } else {
                this.error_img_code = true;
            }

        },
        // 表单提交
        on_submit: function(){
            this.check_username();
            this.check_pwd();
            this.check_image_code();

            if (this.error_username == true || this.error_password == true || this.error_img_code == true || this.veri_img_code == true) {
                // 不满足登录条件：禁用表单
                alert("输入信息有误");
				window.event.returnValue = false
            }
        }
    }
});
