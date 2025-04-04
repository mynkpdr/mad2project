export function useDateFormatter() {
    const formatDate1 = (unixTimestamp) => {
      if (unixTimestamp === null) return null;
      const date = new Date(unixTimestamp * 1000);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
    };
  
    const formatDate2 = (unixTimestamp) => {
      if (unixTimestamp === null) return null;
      const date = new Date(unixTimestamp * 1000);
      const year = date.getFullYear();
      const monthNames = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
      ];
      const month = monthNames[date.getMonth()];
      const day = String(date.getDate()).padStart(2, "0");
      const hours = date.getHours();
      const minutes = String(date.getMinutes()).padStart(2, "0");
      const ampm = hours >= 12 ? "PM" : "AM";
      const formattedHours = String(hours % 12 || 12).padStart(2, "0");
      return `${month} ${day}, ${year} ${formattedHours}:${minutes} ${ampm}`; // MMMM DD, YYYY hh:mm A
    };
  
    const formatTimeAgo = (unixTimestamp) => {
      if (unixTimestamp === null) return null;
      const date = new Date(unixTimestamp * 1000);
      const currentDate = new Date();
      const diff = currentDate - date;
      const seconds = Math.floor(diff / 1000);
      const minutes = Math.floor(seconds / 60);
      const hours = Math.floor(minutes / 60);
      const days = Math.floor(hours / 24);
      const months = Math.floor(days / 30);
      const years = Math.floor(months / 12);
      if (years > 0) {
        return `${years} year${years > 1 ? "s" : ""} ago`;
      } else if (months > 0) {
        return `${months} month${months > 1 ? "s" : ""} ago`;
      } else if (days > 0) {
        return `${days} day${days > 1 ? "s" : ""} ago`;
      } else if (hours > 0) {
        return `${hours} hour${hours > 1 ? "s" : ""} ago`;
      } else if (minutes > 0) {
        return `${minutes} minute${minutes > 1 ? "s" : ""} ago`;
      } else {
        return `${seconds} second${seconds > 1 ? "s" : ""} ago`;
      }
    }

    const formatTimeTaken = (seconds) => {
      if (seconds === null) return null;
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      const hours = Math.floor(minutes / 60);
      const remainingMinutes = minutes % 60;
      if (hours > 0) {
        return `${hours} hour${hours > 1 ? "s" : ""}` + (remainingMinutes > 0 ? ` ${remainingMinutes} minute${remainingMinutes > 1 ? "s" : ""}` : "");
      } else if (minutes > 0) {
        return remainingSeconds === 0 ? `${minutes} minute${minutes > 1 ? "s" : ""}` : `${minutes} minute${minutes > 1 ? "s" : ""} ${remainingSeconds} second${remainingSeconds > 1 ? "s" : ""}`;
      } else {
        return `${seconds} second${seconds > 1 ? "s" : ""}`;
      }
    };

    const convertToISOFormat = (unixTimestamp) => {
      if (unixTimestamp === null) return null;
      const date = new Date(unixTimestamp * 1000);
      date.setMinutes(date.getMinutes() + 330); // Adjust for Indian Standard Time (IST)
      return date.toISOString().slice(0, 16);
    }

    const minDate = () => {
      const date = new Date()
      date.setMinutes(date.getMinutes() + 330)
      return date.toISOString().slice(0, 16)
    };
    
    
  
    return { formatDate1, formatDate2, formatTimeAgo, convertToISOFormat, minDate, formatTimeTaken };
  }
  