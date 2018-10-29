    var htmlWebpackPlugin = require('html-webpack-plugin');
var path = require('path');
console.log(__dirname);
module.exports = {
    /*context: __dirname,*/
//    entry: './src/app.js',
 entry: path.resolve(__dirname, 'javascripts', 'main.js')

    output: {
        path: './dist',
        filename: 'js/[name]-bound.js'//生成后的文件名 为 a-2ea5b2e9b258a8bbba73.js，main-2ea5b2e9b258a8bbba73.js
    },
    module: {
        loaders: [
            {
                test: /\.js$/,
                loader: 'babel-loader',
                /*exclude: path.resolve(__dirname, 'node_modules'), //编译时，不需要编译哪些文件*/
                /*include: path.resolve(__dirname, 'src'),//在config中查看 编译时，需要包含哪些文件*/
                query: {
                    presets: ['latest'] //按照最新的ES6语法规则去转换
                }
            }
        ],
//        rules: [
//            {
//                test: /\.worker\.js$/,
//                use: { loader: 'worker-loader' }
//            }
//        ]
        rules: [
            {
                test: /\.vue$/,
                    use: [
                        {
                            loader: 'vue-loader',
                            options: {

                            }
                        },
                        {
                            loader: 'iview-loader',
                            options: {
                            prefix: false
                        }
                    }
                ]
            }
        ]


    },
    plugins: [
        new htmlWebpackPlugin({
            filename: 'index.html', //通过模板生成的文件名
            template: 'index.html',//模板路径
            inject: 'body' //是否自动在模板文件添加 自动生成的js文件链接

        })
    ]
};