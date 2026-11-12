import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=process.argv[2],out=process.argv[3];
const book=JSON.parse(await fs.readFile(process.argv[4]||`${root}/templates/graph-10.json`,'utf8'));
const schema=JSON.parse(await fs.readFile(`${root}/schemas/graph.schema.json`,'utf8'));
const wb=Workbook.create();
for(const [name,records] of Object.entries(book)){
 const headers=schema.properties[name]['x-column-order'],sheet=wb.worksheets.add(name);
 const range=sheet.getRangeByIndexes(0,0,records.length+1,headers.length);
 range.format.numberFormat='@';
 range.values=[headers,...records.map(r=>headers.map(h=>r[h]))];
 range.format.font={name:'Arial',size:10,color:'#111111'};range.format.wrapText=true;range.format.verticalAlignment='top';range.format.columnWidth=28;
 sheet.getRangeByIndexes(0,0,1,headers.length).format.fill='#EEEEEE';sheet.getRangeByIndexes(0,0,1,headers.length).format.font.bold=true;
 for(const field of ['content','evidence','manifest']){const col=headers.indexOf(field);if(col>=0)sheet.getRangeByIndexes(0,col,records.length+1,1).format.columnWidth=80;}
 range.format.autofitRows();sheet.freezePanes.freezeRows(1);sheet.showGridLines=false;
}
wb.recalculate();await fs.mkdir(out,{recursive:true});
for(const name of Object.keys(book)){
 const blob=await wb.render({sheetName:name,range:name==='Nodes'?'D1:H3':name==='Edges'?'F1:J3':name==='History'?'C1:G3':'A1:D3',scale:1,format:'png'});
 await fs.writeFile(`${out}/${name}.png`,new Uint8Array(await blob.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(`${out}/yori-lite-graph-${book.Nodes.length}.xlsx`);
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:1600})).ndjson);
