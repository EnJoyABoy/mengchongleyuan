var vm = new Vue({
    el: '#app',
	// 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        error_contents: false,
        error_time: false,
        error_address: false,
		error_contents_message: '请输入您的需求',
		error_time_message: '请输入您需要需求的时间',
		error_address_message: '请输入详细地址',
        contents: '',
        district: '',
        address: '',
    },
    methods: {
        // 检查内容是否为空
        check_contents: function(){
			if (this.contents) {
                this.error_contents = false;
            } else {
                this.error_contents = true;
            }
        },
		// 检查时间是否为空
        check_time: function(){
			if (this.time) {
                this.error_time = false;
            } else {
                this.error_time = true;
            }
        },
		// 检查详细地址是否为空
        check_address: function(){
			if (this.address) {
                this.error_address = false;
            } else {
                this.error_address = true;
            }
        },
        // 表单提交
        on_submit: function(){
            this.check_contents();
            this.check_time();
            this.check_address();

            if (this.error_contents == true || this.error_time == true || this.error_address == true) {
                // 不满足登录条件：禁用表单
				window.event.returnValue = false
            }
        }
    }
});
