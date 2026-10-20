"""Helper de M4: toda consulta HTTP pasa por get(); guarda la respuesta cruda en datos/ y registra URL, parámetros y fecha en datos/log_consultas.jsonl.
Sin secuencias de EPILAB; solo identificadores públicos y texto de consulta."""
import requests, json, os, time, datetime, hashlib
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, 'datos')
LOG = os.path.join(DATOS, 'log_consultas.jsonl')
S = requests.Session()
S.headers['User-Agent'] = 'python-requests (academic literature/structure coverage survey)'

def get(url, params=None, name=None, kind='json', method='GET', body=None, timeout=60, retries=2, note=''):
    last = None
    for i in range(retries + 1):
        try:
            if method == 'GET':
                r = S.get(url, params=params, timeout=timeout)
            else:
                r = S.post(url, params=params, json=body, timeout=timeout)
            break
        except Exception as e:
            last = e; time.sleep(2)
    else:
        rec = dict(ts=datetime.datetime.utcnow().isoformat() + 'Z', url=url, params=params, body=body, method=method, error=repr(last), name=name, note=note)
        open(LOG, 'a').write(json.dumps(rec, ensure_ascii=False) + '\n')
        raise last
    ct = r.headers.get('content-type', '')
    fn = None
    if name:
        ext = 'json' if kind == 'json' else ('xml' if kind == 'xml' else ('fasta' if kind == 'fasta' else 'txt'))
        fn = f'{name}.{ext}'
        with open(os.path.join(DATOS, fn), 'wb') as f:
            f.write(r.content)
    rec = dict(ts=datetime.datetime.utcnow().isoformat() + 'Z', method=method, url=r.url if method == 'GET' else url, params=params if method != 'GET' else None,
               body=body, status=r.status_code, bytes=len(r.content), file=fn, content_type=ct, name=name, note=note)
    open(LOG, 'a').write(json.dumps(rec, ensure_ascii=False) + '\n')
    return r
