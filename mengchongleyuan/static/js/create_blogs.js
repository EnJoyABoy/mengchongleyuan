var vm = new Vue({
    el: '#app',
	// 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host,
        error_contents: false,
        error_time: false,
        error_address: false,
        create_blog: false,
		error_contents_message: '请输入您的需求',
		error_time_message: '请输入您需要需求的时间',
		error_address_message: '请输入详细地址',
        contents: '',
        time: '',
        address: '',
        username: '',
        provinces: [],
        cities: [],
        districts: [],
        count: 0,
        form_address: {
            province_id: '',
            city_id: '',
            district_id: '',
        }
    },
        mounted(){
        // 获取省份数据
        this.get_provinces();
        // 获取博客数量
        this.get_count_blog();
        this.username=getCookie('username');
    },
    watch: {
        // 监听到省份id变化
        'form_address.province_id': function () {
            if (this.form_address.province_id) {
                var url = this.host + '/areas/?area_id=' + this.form_address.province_id;
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.code == '0') {
                            // this.cities = response.data.sub_data.subs;
                            this.cities = response.data.sub_data;
                        } else {
                            console.log(response.data);
                            this.cities = [];
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                        this.cities = [];
                    });
            }
        },
        // 监听到城市id变化
        'form_address.city_id': function () {
            if (this.form_address.city_id) {
                var url = this.host + '/areas/?area_id=' + this.form_address.city_id;
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.code == '0') {
                            // this.districts = response.data.sub_data.subs;
                            this.districts = response.data.sub_data;
                        } else {
                            console.log(response.data);
                            this.districts = [];
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                        this.districts = [];
                    });
            }
        }
    },
    methods: {
        // 获取省份数据
        get_provinces(){
            var url = this.host + '/areas/';
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    if (response.data.code == '0') {
                        this.provinces = response.data.province_list;
                    } else {
                        console.log(response.data);
                        this.provinces = [];
                    }
                })
                .catch(error => {
                    console.log(error.response);
                    this.provinces = [];
                });
        },
        // 获取当前用户的博客数
        get_count_blog(){
            var url = this.host + '/getcountblog/';
            axios.get(url, {
                responseType: 'json'
            }).then(response => {
                if (response.data.code == '0') {
                    this.count = response.data.count
                } else {
                    console.log(response.data);
                }
            }).catch(error => {
                console.log(error.response);
            })
        },
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
        // 检测博客数量，限制最多只能发布5条
        check_blog: function (){
            if (this.count >= 5){
                alert("最多只能发布5条需求");
                this.create_blog = true;
            } else {
                this.create_blog = false;
            }
        },
        // 表单提交
        on_submit: function(){
            this.check_contents();
            this.check_time();
            this.check_address();
            this.check_blog();

            if (this.error_contents == true || this.error_time == true || this.error_address == true || this.create_blog == true) {
                // 不满足登录条件：禁用表单
				window.event.returnValue = false
            }
        }
    }
});
