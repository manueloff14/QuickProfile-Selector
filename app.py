from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'clave_secreta'

conn = sqlite3.connect('clicks.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS fotos (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             nombre TEXT,
             imagen TEXT,
             clicks INTEGER DEFAULT 0)''')
conn.commit()
conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('clicks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM fotos ORDER BY RANDOM() LIMIT 2")
    fotos = c.fetchall()
    conn.close()
    return render_template('index.html', fotos=fotos)

@app.route('/clic/<int:selected_id>/<int:skipped_id>')
def clic(selected_id, skipped_id):
    conn = sqlite3.connect('clicks.db')
    c = conn.cursor()
    c.execute("UPDATE fotos SET clicks = clicks + 1 WHERE id = ?", (selected_id,))
    conn.commit()
    c.execute("SELECT * FROM fotos WHERE id = ?", (skipped_id,))
    skipped_foto = c.fetchone()
    c.execute("SELECT * FROM fotos WHERE id != ? ORDER BY RANDOM() LIMIT 1", (skipped_id,))
    new_foto = c.fetchone()
    conn.close()
    return redirect(url_for('index'))

@app.route('/omitir', methods=['POST'])
def omitir():
    skipped_id = request.form['skipped_id']
    conn = sqlite3.connect('clicks.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM fotos WHERE id < ?", (skipped_id,))
    count = c.fetchone()[0]
    if count % 3 == 0:
        enable_skip = True
    else:
        enable_skip = False
    c.execute("SELECT * FROM fotos WHERE id != ? ORDER BY RANDOM() LIMIT 2", (skipped_id,))
    fotos = c.fetchall()
    conn.close()
    return render_template('index.html', fotos=fotos, enable_skip=enable_skip)

@app.route('/subir', methods=['GET', 'POST'])
def subir():
    if request.method == 'POST':
        nombre = request.form['nombre']
        imagen = request.files['imagen']
        if imagen.filename != '':
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], imagen.filename)
            imagen.save(img_path)
            conn = sqlite3.connect('clicks.db')
            c = conn.cursor()
            c.execute("INSERT INTO fotos (nombre, imagen) VALUES (?, ?)", (nombre, img_path))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/editar', methods=['GET'])
def lista_personas():
    conn = sqlite3.connect('clicks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM fotos")
    fotos = c.fetchall()
    conn.close()
    return render_template('editar_lista.html', fotos=fotos)

@app.route('/editar/<int:foto_id>', methods=['GET', 'POST'])
def editar(foto_id):
    if request.method == 'POST':
        nuevo_nombre = request.form['nuevo_nombre']
        nueva_imagen = request.files['nueva_imagen']
        if nueva_imagen.filename != '':
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], nueva_imagen.filename)
            nueva_imagen.save(img_path)
            conn = sqlite3.connect('clicks.db')
            c = conn.cursor()
            c.execute("UPDATE fotos SET nombre = ?, imagen = ? WHERE id = ?", (nuevo_nombre, img_path, foto_id))
            conn.commit()
            conn.close()
            return redirect(url_for('estadisticas'))
        return redirect(url_for('editar', foto_id=foto_id))  # Redirecciona si no hay imagen seleccionada
    else:
        conn = sqlite3.connect('clicks.db')
        c = conn.cursor()
        c.execute("SELECT * FROM fotos WHERE id = ?", (foto_id,))
        foto = c.fetchone()
        conn.close()
        return render_template('editar.html', foto=foto)

@app.route('/eliminar/<int:foto_id>', methods=['POST'])
def eliminar(foto_id):
    conn = sqlite3.connect('clicks.db')
    c = conn.cursor()
    c.execute("DELETE FROM fotos WHERE id = ?", (foto_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('lista_personas'))

@app.route('/estadisticas')
def estadisticas():
    conn = sqlite3.connect('clicks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM fotos ORDER BY clicks DESC")
    fotos = c.fetchall()
    conn.close()
    return render_template('statistics.html', fotos=fotos)

if __name__ == '__main__':
    app.run(debug=True)
