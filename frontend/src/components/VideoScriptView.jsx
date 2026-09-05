import React, { useState } from 'react';
import { apiService } from '../services/api';
import { FileVideo, Copy, Save, Download, Loader2, Check } from 'lucide-react';

export default function VideoScriptView() {
  const [formData, setFormData] = useState({
    topic: '',
    format: 'Video ngắn (TikTok/Reels/Shorts: 30s - 60s)',
    tone: 'Chuyên gia uy tín, gần gũi, thực tế',
    audience: 'Giới văn phòng, người bận rộn'
  });
  const [script, setScript] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!formData.topic.trim()) return;
    
    setLoading(true);
    setScript('');
    try {
      const response = await apiService.generateVideoScript(formData);
      setScript(response.script);
    } catch (err) {
      console.error(err);
      alert('Đã xảy ra lỗi khi tạo kịch bản. Vui lòng thử lại.');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (!script) return;
    navigator.clipboard.writeText(script);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    if (!script) return;
    const blob = new Blob([script], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = Kich_ban_.md;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="p-4 bg-transparent text-gray-100 min-h-[calc(100vh-80px)] overflow-y-auto pb-20">
      <div className="flex items-center gap-3 mb-6">
        <FileVideo className="text-blue-400" size={28} />
        <h2 className="text-2xl font-bold text-white">Viết Kịch Bản Video</h2>
      </div>

      <div className="bg-[#1e293b]/80 backdrop-blur-md rounded-2xl p-6 shadow-lg border border-white/10 mb-6">
        <form onSubmit={handleGenerate} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Chủ đề / Ý tưởng (Từ khóa)</label>
            <input 
              type="text" 
              name="topic" 
              value={formData.topic} 
              onChange={handleInputChange} 
              placeholder="Vd: 3 loại thực phẩm cần tránh cho người Gout..." 
              className="w-full p-3 bg-white/5 text-gray-100 border border-white/10 rounded-xl focus:outline-none focus:border-blue-500 transition-colors"
              required 
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Định dạng Video</label>
            <select 
              name="format" 
              value={formData.format} 
              onChange={handleInputChange} 
              className="w-full p-3 bg-gray-800 text-gray-100 border border-white/10 rounded-xl focus:outline-none focus:border-blue-500"
            >
              <option>Video ngắn (TikTok/Reels/Shorts: 30s - 60s)</option>
              <option>Video chuyên sâu (YouTube: 3 - 5 phút)</option>
              <option>Video dài (YouTube Podcast: 8 - 10 phút)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Phong cách (Tone & Voice)</label>
            <input 
              type="text" 
              name="tone" 
              value={formData.tone} 
              onChange={handleInputChange} 
              placeholder="Vd: Chuyên gia uy tín, dí dỏm..." 
              className="w-full p-3 bg-white/5 text-gray-100 border border-white/10 rounded-xl focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Đối tượng người xem</label>
            <input 
              type="text" 
              name="audience" 
              value={formData.audience} 
              onChange={handleInputChange} 
              placeholder="Vd: Dân văn phòng ngồi nhiều..." 
              className="w-full p-3 bg-white/5 text-gray-100 border border-white/10 rounded-xl focus:outline-none focus:border-blue-500"
            />
          </div>

          <button 
            type="submit" 
            disabled={loading || !formData.topic.trim()}
            className="w-full py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold rounded-xl shadow-lg flex items-center justify-center gap-2 transition-all disabled:opacity-50"
          >
            {loading ? <Loader2 className="animate-spin" size={20} /> : <FileVideo size={20} />}
            {loading ? 'Đang viết kịch bản...' : 'Tạo Kịch Bản Bằng AI'}
          </button>
        </form>
      </div>

      {script && (
        <div className="bg-[#1e293b]/80 backdrop-blur-md rounded-2xl shadow-lg border border-white/10 overflow-hidden animate-fade-in">
          <div className="flex items-center justify-between p-4 bg-white/5 border-b border-white/10">
            <h3 className="font-bold text-blue-400">Kết Quả Kịch Bản</h3>
            <div className="flex gap-2">
              <button onClick={handleCopy} className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-colors flex items-center gap-1 text-sm text-gray-200">
                {copied ? <Check size={16} className="text-green-400" /> : <Copy size={16} />}
                <span className="hidden sm:inline">{copied ? 'Đã copy' : 'Copy'}</span>
              </button>
              <button onClick={handleDownload} className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-colors flex items-center gap-1 text-sm text-gray-200">
                <Download size={16} />
                <span className="hidden sm:inline">Lưu .MD</span>
              </button>
            </div>
          </div>
          <div className="p-6 overflow-x-auto">
            <div className="whitespace-pre-wrap font-sans text-gray-200 leading-relaxed" style={{ fontSize: '15px' }}>
              {script}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
