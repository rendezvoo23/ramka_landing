const port = process.env.PORT || 4173;

module.exports = {
  apps: [
    {
      name: "ramka-landing",
      cwd: __dirname,
      script: "./node_modules/vite/bin/vite.js",
      args: `preview --host 0.0.0.0 --port ${port}`,
      instances: 2,
      exec_mode: "cluster",
      watch: false,
      env: {
        NODE_ENV: "production",
        PORT: port,
      },
    },
  ],
};
