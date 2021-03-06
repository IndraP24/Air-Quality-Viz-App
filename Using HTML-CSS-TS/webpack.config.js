var $path = require("path");
const regeneratorRuntime = require("regenerator-runtime/runtime");

module.exports = {
    mode: "production",

    devtool: "source-map",

    entry: {
        index: "./src/index.ts"
    },

    output: {
        path: $path.join(__dirname, "dist"),
        filename: "[name].js",
        chunkFilename: "[name].js",
        publicPath: "/dist/"
    },

    module: {
        rules: [{
            test: /\.js$/,
            include: /node_modules/,
            use: {
                loader: "babel-loader",
                options: {
                    presets: ["@babel/preset-env"],
                    plugins: ["@babel/plugin-syntax-dynamic-import"]
                }
            }
        }, {
            test: /.js$/,
            use: ["source-map-loader"],
            enforce: "pre"
        }]
    }
};