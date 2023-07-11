var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host: host,
        error_name: false,
        error_password: false,
        error_check_password: false,
        error_mobile: false,
        error_image_code: false,
        error_sms_code: false,
        error_allow: false,
        error_name_message: '请输入5-20个字符的用户',
        error_password_message: '请输入8-20位的密码',
        error_password2_message: '两次输入的密码不一致',
        error_mobile_message: '请输入正确的手机号码',
        error_image_code_message: '请填写图形验证码',
        error_sms_code_message: '请填写短信验证码',
        error_allow_message: '请勾选用户协议',
        image_code_id: '',
        image_code_url: '',
        sms_code_tip: '获取短信验证码',
        sending_flag: false,
        username: '',
        password: '',
        password2: '',
        mobile: '',
        image_code: '',
        sms_code: '',
        allow: true
    },
    methods: {
        // 检查用户名
        check_username: function () {
            // alert('验证用户名');
            var re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)) {
                this.error_name = false;
            } else {
                this.error_name_message = '请输入5-20个字符的用户名';
                this.error_name = true;

            }

        //    在这里发送一个axios 请求
        //    1.组织url
            let url = '/usernames/'+this.username+'/count/';
        //    2.发送请求
            axios.get(url).then(response=>{
                //    3.请求成功的回调的业务逻辑
                // console.log(response)
                if(response.data.count == 0){
                    this.error_name=false
                }else{
                    this.error_name=true;
                    this.error_name_message='用户名已注册';
                }
            }).catch(error=>{

            })
        },
        // 检查密码
        check_password: function () {
            var re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        // 确认密码
        check_password2: function () {
            if (this.password != this.password2) {
                this.error_check_password = true;
            } else {
                this.error_check_password = false;
            }
        },
        // 检查手机号
        check_mobile: function () {
            var re = /^1[3456789]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile_message = '您输入的手机号格式不正确';
                this.error_mobile = true;
            }
            //    在这里发送一个axios 请求
            //    1.组织url
            let url = '/usermobile/'+this.mobile+'/count/';
            //    2.发送请求
            axios.get(url).then(response=>{
                //    3.请求成功的回调的业务逻辑
                // console.log(response)
                if(response.data.count == 0){
                    this.error_mobile=false
                }else{
                    this.error_mobile=true;
                    this.error_mobile_message='手机号已注册';
                }
            }).catch(error=>{

            })
        },
        // 表单提交
        on_submit(){
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();

            if (this.error_name == true || this.error_password == true || this.error_check_password == true
                || this.error_mobile == true) {
                // 不满足注册条件：禁用表单
                window.event.returnValue = false;
            }
        }

    }
});
