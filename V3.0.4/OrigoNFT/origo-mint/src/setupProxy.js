const { createProxyMiddleware } = require('http-proxy-middleware');
console.log("2 index.js");
module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:3001',
      changeOrigin: true,
    })
  );
};
console.log("12 index.js");