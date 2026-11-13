"""Offline size/index benchmark, never a Claude latency claim."""
import json,sys,time,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import fast_cortex as f
sizes=[]
for n in (10,1000,10000):
 rows=f.fixture(n);t=time.perf_counter();idx=f.Index(rows);cold=(time.perf_counter()-t)*1000
 times=[]
 for _ in range(100):
  t=time.perf_counter();assert idx.topic(f'topic/{n-2}');assert idx.neighbors('fixture0:1');times.append((time.perf_counter()-t)*1000)
 # High-degree fixture neighbors are intentionally O(N), not hidden by a cap.
 sizes.append({'nodes':n,'physical_rows':len(rows),'cold_index_ms':round(cold,3),'warm_topic_plus_all_high_degree_edges_median_ms':round(statistics.median(times),3),'index_cells_A_I':9*len(rows),'remote_calls':'not measured'})
pair=[['b65ab37ff49046dfa95096f7a326d9ab',1,2,'NODE','','','People','person-A/favorite_color','','Blue.','person-A','S','Person: my favorite color is blue.'],['b65ab37ff49046dfa95096f7a326d9ab',2,2,'EDGE','','','about','b65ab37ff49046dfa95096f7a326d9ab:1','person-A','Person stated this preference.','person-A','S','Same statement.']]
args={'spreadsheetId':'1gwmwmnscN0suFKzp8RHKqb9qrSwRvnpoykCZr43veqk','range':'Memory!A1','values':pair}
size=lambda separators:len(json.dumps(args,ensure_ascii=False,separators=separators).encode())
result={'measurement':'Local serialization and Python index time; not Claude or Sheets performance','payload_compact_bytes':size((',',':')),'payload_default_spacing_bytes':size((', ',': ')),'user_reported_previous_compact_graph_bytes':3857,'payload_reduction_percent':round(100*(3857-size((',',':')))/3857,1),'scale':sizes,'warm_remote_strategy':'tail refresh plus ID/topic/endpoint maps; cold range-only chats scan index once'}
root=Path(__file__).resolve().parents[1];(root/'tests/FAST_BENCHMARK.json').write_text(json.dumps(result,indent=2)+'\n')
Path('/tmp/yori-fast-build/scale.json').write_text(json.dumps(f.fixture(1000)[1:]))
print(json.dumps(result,indent=2))
