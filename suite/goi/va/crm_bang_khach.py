"""Vá giao diện CRM (gói Web CRM + Lead Page) trước khi đóng vào TISA BOT.

Chủ yêu cầu 10/11/2026: bảng Data Zalo / FB có cột STT đầu tiên, rồi Ngày đăng ký (ngày/tháng/năm + giờ), rồi Khách...
Mỗi mục: (tệp trong crm-source.zip, [(chuỗi cũ, chuỗi mới), ...]). Chuỗi cũ phải có đúng 1 lần, không thì build dừng.
"""
VA = [
    ("client/src/components/ChatbotLeads.tsx", [
        ('w-[1980px] table-fixed', 'w-[1906px] table-fixed'),
        ('[200,140,200,230,230,70,145,145,170,170,180].map', '[56,150,200,140,200,230,230,70,145,145,170,170].map'),
        ("""{['Khách','SĐT','Email','Sản phẩm quan tâm','Lo lắng','DISC','Tiềm năng (AI)','Trạng thái','Sale phụ trách','Doanh thu chốt','Ngày'].map((h,i)=><th style={i===0?{position:"sticky",left:0,zIndex:30}:undefined} key={h} scope="col" aria-sort={i===6||i===10?(sort===(i===6?'potential':'date')?(direction==='desc'?'descending':'ascending'):'none'):undefined} className={'whitespace-nowrap border-b border-slate-200 bg-slate-100 px-3 py-3 '+(i===0?'sticky left-0 z-30 w-[200px] min-w-[200px]':'')}>{i===6||i===10?<button onClick={()=>toggleSort(i===6?'potential':'date')} className="py-1" aria-label={'Sắp xếp theo '+h}>{h} {sort===(i===6?'potential':'date')?(direction==='desc'?'↓':'↑'):'↕'}</button>:h}</th>)}""",
         """{['STT','Ngày đăng ký','Khách','SĐT','Email','Sản phẩm quan tâm','Lo lắng','DISC','Tiềm năng (AI)','Trạng thái','Sale phụ trách','Doanh thu chốt'].map((h,i)=>{const sx=i===1||i===8,khoa=i===8?'potential':'date';return <th style={i===0?{position:"sticky",left:0,zIndex:30}:i===2?{position:"sticky",left:56,zIndex:30}:undefined} key={h} scope="col" aria-sort={sx?(sort===khoa?(direction==='desc'?'descending':'ascending'):'none'):undefined} className={'whitespace-nowrap border-b border-slate-200 bg-slate-100 px-3 py-3 '+(i===0?'text-center':'')}>{sx?<button onClick={()=>toggleSort(khoa)} className="py-1" aria-label={'Sắp xếp theo '+h}>{h} {sort===khoa?(direction==='desc'?'↓':'↑'):'↕'}</button>:h}</th>})}"""),
        ("""{rows.map(r=><tr key={r.id} onClick={()=>open(r.id)} className="group cursor-pointer hover:bg-blue-50">
 <td style={{position:"sticky",left:0,zIndex:10}} className="sticky left-0 z-10 border-b border-slate-100 bg-white px-3 py-3 group-hover:bg-blue-50"><button""",
         """{rows.map((r,i)=><tr key={r.id} onClick={()=>open(r.id)} className="group cursor-pointer hover:bg-blue-50">
 <td style={{position:"sticky",left:0,zIndex:10}} className="border-b border-slate-100 bg-white px-2 py-3 text-center font-semibold text-slate-500 group-hover:bg-blue-50">{(page-1)*20+i+1}</td>
 <td className="border-b border-slate-100 px-3 py-3 whitespace-nowrap"><div className="font-semibold text-slate-800">{new Date(r.created_at).toLocaleDateString('vi-VN',{timeZone:'Asia/Ho_Chi_Minh',day:'2-digit',month:'2-digit',year:'numeric'})}</div><div className="text-xs text-slate-500">{new Date(r.created_at).toLocaleTimeString('vi-VN',{timeZone:'Asia/Ho_Chi_Minh',hour:'2-digit',minute:'2-digit'})}</div></td>
 <td style={{position:"sticky",left:56,zIndex:10}} className="border-b border-slate-100 bg-white px-3 py-3 shadow-[2px_0_0_0_rgb(241,245,249)] group-hover:bg-blue-50"><button"""),
        ("""<td className="border-b border-slate-100 px-3 py-3 whitespace-nowrap" title={new Date(r.created_at).toLocaleString('vi-VN',{timeZone:'Asia/Ho_Chi_Minh'})}>{new Date(r.created_at).toLocaleDateString('vi-VN',{timeZone:'Asia/Ho_Chi_Minh'})}</td>""", ""),
    ]),
]


def ap(ten, chu):
    """Áp vá cho một tệp. Trả chuỗi mới, hoặc nguyên chuỗi nếu tệp không có trong VA."""
    for f, ds in VA:
        if f != ten:
            continue
        for cu, moi in ds:
            if chu.count(cu) != 1:
                raise SystemExit("DỪNG: vá CRM %s không khớp (%d lần): %s" % (f, chu.count(cu), cu[:80]))
            chu = chu.replace(cu, moi)
    return chu
