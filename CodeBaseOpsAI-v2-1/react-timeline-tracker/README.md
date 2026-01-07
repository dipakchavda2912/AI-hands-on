# React Timeline Tracker

A beautiful timeline progress tracker built with React 18.3, matching the design from the screenshot with horizontal milestones and vertical subtasks.

## Features

- ✨ **Horizontal Timeline** - Visual milestone progression with dates
- 📋 **Vertical Subtasks** - Detailed subtask progress for each milestone
- 🎨 **Status Colors** - Color-coded status indicators (Green, Yellow, Red, Gray)
- 🎯 **Real-time Progress** - Live updates as tasks progress
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🎉 **Animations** - Smooth transitions and pulse effects

## Tech Stack

- React 18.3.1
- React Scripts 5.0.1
- CSS3 with animations
- Modern ES6+ JavaScript

## Installation

### Prerequisites

- Node.js 16.x or higher
- npm 8.x or higher

### Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

3. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

### Serve Production Build

```bash
npm install -g serve
serve -s build
```

## Project Structure

```
react-timeline-tracker/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/
│   │   ├── Timeline.js     # Main timeline component
│   │   └── Timeline.css    # Timeline styles
│   ├── App.js              # App component
│   ├── App.css             # App styles
│   ├── index.js            # Entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies and scripts
└── README.md              # This file
```

## Usage

Click the "Start Execution" button to begin the timeline progression. The application will:

1. Progress through each milestone sequentially
2. Display subtasks for the active milestone
3. Update status with color coding:
   - 🟢 **Green** - Completed
   - 🟡 **Yellow** - In Progress
   - 🔴 **Red** - Error (randomly simulated)
   - ⚪ **Gray** - Pending

## Customization

### Modify Tasks

Edit the `tasks` array in `src/components/Timeline.js`:

```javascript
const tasks = [
  {
    name: "Your Task Name",
    shortName: "Short Name",
    date: "Jan 20",
    description: "Task description",
    note: {
      date: "Feb 5",
      text: "Note text",
      subtext: "Additional info",
      type: "green" // or "red"
    },
    subtasks: [
      "Subtask 1",
      "Subtask 2",
      "Subtask 3"
    ]
  },
  // Add more tasks...
];
```

### Adjust Animation Speed

Modify the `sleep()` duration in the `startExecution()` function:

```javascript
await sleep(500); // Milliseconds (500ms = 0.5 seconds)
```

### Change Colors

Edit the CSS variables in `src/components/Timeline.css`:

```css
/* Green color */
#48bb78

/* Yellow/Orange color */
#f6ad55

/* Red color */
#f56565

/* Gray color */
#cbd5e0
```

## Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

## Technologies Used

- **React** 18.2.0 - UI library
- **CSS3** - Styling with animations and transitions
- **JavaScript ES6+** - Modern JavaScript features

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Author

Created as a timeline progress tracker UI component.
