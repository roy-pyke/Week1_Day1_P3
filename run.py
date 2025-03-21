from app import create_app, db

app = create_app()

# 在应用上下文中创建所有数据库表（如果尚未创建）
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # 调试模式下启动应用，生产环境请关闭 debug 模式
    app.run(debug=True, port=5005)