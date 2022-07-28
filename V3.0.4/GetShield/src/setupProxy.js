const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://35.85.50.164:3000',
      changeOrigin: true,
    })
  );
};
