# Knowledge-base Search Engine - Frontend

React-based frontend for the Knowledge-base Search Engine with RAG capabilities.

## 🚀 Quick Start

### Prerequisites

- Node.js 16+ and npm
- Backend API running on `http://localhost:8000`

### Installation

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## 🎨 Features

- **Drag & Drop Upload**: Easy document upload with visual feedback
- **Real-time Query Interface**: Ask questions with advanced options
- **Results Display**: AI-generated answers with source citations
- **Database Statistics**: Monitor your knowledge base
- **Responsive Design**: Works on desktop and mobile
- **Copy to Clipboard**: Easy sharing of results

## 📁 Components

- `App.js` - Main application with tab navigation
- `FileUpload.js` - Document upload with drag & drop
- `QueryInterface.js` - Question input with advanced options
- `ResultsDisplay.js` - Answer display with source citations
- `StatsDisplay.js` - Database statistics and monitoring

## 🎯 Usage

1. **Upload Documents**: Go to the "Upload Documents" tab and drag & drop PDF or TXT files
2. **Ask Questions**: Use the "Ask Questions" tab to query your documents
3. **View Results**: See AI-generated answers with source citations
4. **Monitor Stats**: Check the "Database Stats" tab for collection information

## 🔧 Configuration

The frontend automatically connects to the backend API. Make sure your backend is running on `http://localhost:8000`.

For production deployment, update the API endpoints in the components.

## 📦 Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build` folder.

## 🧪 Testing

```bash
npm test
```

## 📱 Responsive Design

The frontend is fully responsive and works on:
- Desktop (1024px+)
- Tablet (768px - 1023px)
- Mobile (320px - 767px)

## 🎨 Styling

Built with Tailwind CSS for:
- Consistent design system
- Responsive utilities
- Custom animations
- Dark/light mode support (future)

## 🔗 API Integration

The frontend integrates with these backend endpoints:
- `POST /upload` - Document upload
- `POST /query` - Question answering
- `GET /stats` - Database statistics
- `GET /health` - Health check

## 🚀 Deployment

### Build and Deploy

1. **Build the application**
   ```bash
   npm run build
   ```

2. **Deploy the `build` folder** to your hosting service:
   - Vercel
   - Netlify
   - AWS S3
   - GitHub Pages

### Environment Variables

For production, you may need to configure:
- `REACT_APP_API_URL` - Backend API URL
- `REACT_APP_MAX_FILE_SIZE` - Maximum file upload size

## 🛠️ Development

### Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

### Code Structure

```
src/
├── components/          # React components
│   ├── FileUpload.js    # Document upload
│   ├── QueryInterface.js # Question input
│   ├── ResultsDisplay.js # Answer display
│   └── StatsDisplay.js  # Statistics
├── App.js              # Main application
├── index.js            # Entry point
└── index.css           # Global styles
```

## 🎯 Future Enhancements

- [ ] Dark mode support
- [ ] File preview before upload
- [ ] Query history
- [ ] Export results
- [ ] Advanced search filters
- [ ] Real-time collaboration
- [ ] Mobile app (React Native)

---

**Built with React, Tailwind CSS, and ❤️**



