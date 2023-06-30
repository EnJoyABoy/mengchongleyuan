var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host,
        username:'',
        blogs:[]
    },
    mounted(){
        // 获取博客数据
        this.get_blogs();
        this.username=getCookie('username');
        console.log(this.username);
    },
    methods: {
        // 获取博客数据
        get_blogs() {
            var url = this.host + '/getmyblogs/';
            axios.get(url, {
                responseType: 'json',
            })
                .then(response => {
                    this.blogs = response.data.blogs;
                })
                .catch(error => {
                    console.log(error.response);
                })
        }
    }
});