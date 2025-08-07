package com.example.photoapp.pages

import android.content.ActivityNotFoundException
import android.content.ContentUris
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import androidx.compose.ui.graphics.asImageBitmap
import android.media.MediaMetadataRetriever
import android.net.Uri
import android.provider.MediaStore
import android.util.Log
import android.widget.Toast
import android.widget.VideoView
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import coil.compose.rememberAsyncImagePainter
import androidx.compose.runtime.*
import androidx.compose.ui.viewinterop.AndroidView


@OptIn(ExperimentalFoundationApi::class)
@Composable
fun GalleryPage(navController: NavController) {
    val context = LocalContext.current

    // This list holds pairs of (URI, type) for each media file (image/video) found on the device
    val mediaList = remember { mutableStateListOf<Pair<Uri, String>>() }

    // Tracks the media items the user has selected — used for sharing via WhatsApp
    val selectedItems = remember { mutableStateListOf<Uri>() }

    // Boolean flag to toggle selection mode (true = selection active, false = browsing mode)
    val selectionMode = remember { mutableStateOf(false) }

    // Holds the URI of the currently previewed image (null means no image is being previewed)
    val previewUri = remember { mutableStateOf<Uri?>(null) }

    // Loads all image and video files from the gallery once when the screen appears
    LaunchedEffect(Unit) {
        mediaList.addAll(loadMediaFromGallery(context))
    }

    // If an image is selected for preview, show it full-screen and hide the gallery UI
    if (previewUri.value != null) {

        if (mediaList.find { it.first == previewUri.value }?.second == "video") {
            VideoPreviewScreen(uri = previewUri.value!!, onBack = { previewUri.value = null })
        } else {
            ImagePreviewScreen(uri = previewUri.value!!, onBack = { previewUri.value = null })
        }

    } else {
        // Main Gallery UI wrapped in a Scaffold, allowing us to add a bottom bar
        Scaffold(
            bottomBar = {
                BottomBar(
                    onHomeClick = { navController.navigate("front") }, // Navigate back to home
                    onShareClick = {
                        // Trigger WhatsApp sharing if any items are selected
                        if (selectedItems.isNotEmpty()) {
                            shareImagesOnWhatsApp(context, selectedItems)
                        }else{
                            Log.e("GalleryPage", "Share button clicked with no selected items")
                        }
                    }
                )
            }
        ) { paddingValues ->

            // Main column layout that fills the entire screen and accounts for scaffold padding
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .background(Color(0xFFF2F0F0)) // Light gray background for aesthetics
            ) {
                // Title bar at the top with gallery title and "Select"/"Cancel" toggle button
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween, // Place title and button far apart
                    verticalAlignment = Alignment.CenterVertically // Center them vertically
                ) {
                    Text(
                        text = "Your Gallery", // Main heading
                        fontSize = 24.sp,
                        fontWeight = FontWeight.SemiBold
                    )

                    // Button toggles selection mode (for multi-select/sharing)
                    Button(
                        onClick = {
                            if (selectionMode.value) {
                                // If cancelling, clear selected items too
                                selectedItems.clear()
                            }
                            selectionMode.value = !selectionMode.value
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color.LightGray)
                    ) {
                        Text(if (selectionMode.value) "Cancel" else "Select")
                    }
                }

                // Section label just above the grid
                Text(
                    text = "BROWSE ALL", // Subheading above media grid
                    fontWeight = FontWeight.Bold,
                    fontSize = 14.sp,
                    modifier = Modifier.padding(start = 16.dp, bottom = 8.dp)
                )

                // Grid that displays all media items (images/videos)
                LazyVerticalGrid(
                    columns = GridCells.Fixed(2), // 2 items per row
                    modifier = Modifier
                        .weight(1f) // Fill available space
                        .padding(horizontal = 8.dp),
                    contentPadding = PaddingValues(bottom = 16.dp) // Space at the bottom
                ) {
                    // Loop over each media item and build its grid tile
                    items(mediaList.size) { index ->
                        val (uri, type) = mediaList[index]

                        // Box representing each image or video tile
                        Box(
                            modifier = Modifier
                                .padding(8.dp)
                                .aspectRatio(1f)
                                .clip(RoundedCornerShape(8.dp))
                                .combinedClickable(
                                    onClick = {
                                        // Normal tap behavior
                                        if (selectionMode.value) {
                                            // Toggle selection
                                            if (selectedItems.contains(uri)) {
                                                //selectedItems.remove(uri)
                                                previewUri.value = uri // Open preview
                                            } else {
                                                selectedItems.add(uri)
                                            }
                                        } else {
                                            // Open preview
                                            if (type == "image") {
                                                previewUri.value = uri
                                            } else {
                                                previewUri.value = uri
                                            }
                                        }
                                    },
                                    onLongClick = {
                                        // Long press to select even if not in selection mode
                                        // If selection mode is off `, enable it
                                        if (!selectionMode.value) {
                                            selectionMode.value = true  // Activates selection mode
                                        }
//                                        // If the long-pressed item is NOT already selected, add it to the selected list
//                                        if (!selectedItems.contains(uri)) {
//                                            selectedItems.add(uri) // Adds the current item's URI to the list of selected items
//                                        }

                                        // Toggle selection:
                                        if (selectedItems.contains(uri)) {
                                            // If already selected, unselect it
                                            selectedItems.remove(uri)
                                        } else {
                                            // If not selected, add it
                                            selectedItems.add(uri)
                                        }

                                    },

                                )
                        ) {

                            // Renders the media thumbnail based on its type
                            if (type == "image") {
                                Image(
                                    painter = rememberAsyncImagePainter(model = uri), // Load image from URI
                                    contentDescription = null,
                                    contentScale = ContentScale.Crop, // Fill tile while preserving crop
                                    modifier = Modifier.fillMaxSize()
                                )
                            }else if (type == "video") {
                                VideoThumbnail(uri)
                            }

                            // If item is selected, draw a white check icon in top-right
                            if (selectedItems.contains(uri)) {
                                Icon(
                                    imageVector = Icons.Default.CheckCircle,
                                    contentDescription = "Selected",
                                    tint = Color.White,
                                    modifier = Modifier
                                        .align(Alignment.TopEnd)
                                        .padding(6.dp)
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun VideoPreviewScreen(uri: Uri, onBack: () -> Unit) {
    val context = LocalContext.current

    // Get the file name (e.g., video.mp4)
    val videoName = remember(uri) {
        getFileNameFromUri(context, uri)
    }

    // Track playback state
    var isPlaying by remember { mutableStateOf(true) }

    // Full-screen container
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black)
    ) {
        // Main vertical layout
        Column(
            modifier = Modifier.fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // 🔙 Back Button at top-left
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Default.ArrowBack,
                    contentDescription = "Back",
                    tint = Color.White,
                    modifier = Modifier
                        .size(30.dp)
                        .clickable { onBack() }
                )
            }

            // 🎬 Full-width Video View (just like image layout)
            AndroidView(
                factory = { ctx ->
                    VideoView(ctx).apply {
                        setVideoURI(uri)
                        setOnPreparedListener {
                            if (isPlaying) start()
                        }
                        setOnCompletionListener {
                            isPlaying = false
                        }
                    }

                },
                update = { videoView ->
                    if (isPlaying) videoView.start() else videoView.pause()
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(550.dp)
                    .padding(horizontal = 16.dp)
                    .clip(RoundedCornerShape(12.dp))
            )

            // ⏯️ Play/Pause Button
            Button(
                onClick = { isPlaying = !isPlaying },
                modifier = Modifier
                    .padding(top = 16.dp)
            ) {
                Text(if (isPlaying) "Pause" else "Play")
            }

            // 🏷️ Video File Name
            Text(
                text = videoName,
                color = Color.White,
                fontSize = 16.sp,
                fontWeight = FontWeight.SemiBold,
                modifier = Modifier
                    .padding(top = 8.dp, bottom = 24.dp)
            )
        }
    }
}

// This function returns the display name (file name including extension, e.g. "video.mp4")
// from a content Uri using Android's ContentResolver.
fun getFileNameFromUri(context: Context, uri: Uri): String {

    // Define the column we want to query from the media store — DISPLAY_NAME holds the filename
    val projection = arrayOf(MediaStore.MediaColumns.DISPLAY_NAME)

    // Query the content resolver to get the file metadata
    context.contentResolver.query(
        uri,               // The content URI of the file
        projection,        // The column(s) we want to retrieve — in this case, just DISPLAY_NAME
        null,              // No selection clause (i.e., no filtering)
        null,              // No selection arguments
        null               // Default sort order
    )?.use { cursor ->     // Auto-close the cursor after use (use block handles closing)

        // Get the index of the DISPLAY_NAME column from the cursor
        val nameIndex = cursor.getColumnIndexOrThrow(MediaStore.MediaColumns.DISPLAY_NAME)

        // Move the cursor to the first row (should be only one in this case)
        if (cursor.moveToFirst()) {
            // Return the actual file name from the DISPLAY_NAME column
            return cursor.getString(nameIndex)
        }
    }

    // Fallback: If the query fails or no result is found, return a default file name
    return "Video"
}

// Extracts a single frame from a video URI to be used as a thumbnail bitmap
fun getVideoThumbnail(context: Context, uri: Uri): Bitmap? {
    return try {
        // Create an instance of MediaMetadataRetriever — used to fetch media metadata or frames
        val retriever = MediaMetadataRetriever()

        // Set the data source using the provided video URI
        retriever.setDataSource(context, uri)

        // Extract a frame at 1 second (1000000 microseconds = 1 second)
        val bitmap = retriever.getFrameAtTime(1000000)

        // Always release the retriever to free resources
        retriever.release()

        // Return the extracted frame as a Bitmap (nullable)
        bitmap
    } catch (e: Exception) {
        // If there's any issue (e.g., file not found, corrupt video), log the error and return null
        e.printStackTrace()
        null
    }
}

@Composable
fun VideoThumbnail(uri: Uri) {
    // Get the current context needed to load the thumbnail from the URI
    val context = LocalContext.current

    // Store the thumbnail bitmap in a state variable so Compose can reactively recompose when it's loaded
    var thumbnail by remember { mutableStateOf<Bitmap?>(null) }

    // Load the thumbnail when the composable first appears or when the URI changes
    LaunchedEffect(uri) {
        // Extract the thumbnail from the video using our helper function
        thumbnail = getVideoThumbnail(context, uri)
    }

    // Outer Box holds the video thumbnail and overlays the Play icon
    Box(modifier = Modifier.fillMaxSize()) {

        // If the thumbnail has been successfully retrieved
        if (thumbnail != null) {
            Image(
                bitmap = thumbnail!!.asImageBitmap(), // Convert Bitmap to Compose ImageBitmap
                contentDescription = null, // No screen reader description needed for thumbnails
                modifier = Modifier.fillMaxSize(), // Fill the grid tile
                contentScale = ContentScale.Crop // Crop to fill the box while maintaining aspect ratio
            )
        } else {
            // If thumbnail is still loading or failed, show a black background placeholder
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black)
            )
        }

        // Overlay a white play icon in the center of the thumbnail to indicate it's a video
        Icon(
            imageVector = Icons.Default.PlayArrow,
            contentDescription = "Video", // Accessibility label for screen readers
            tint = Color.White,
            modifier = Modifier
                .align(Alignment.Center) // Center the icon within the Box
                .size(90.dp) // Icon size
        )
    }
}

// Loads both image and video URIs from the device's external storage using MediaStore
fun loadMediaFromGallery(context: Context): List<Pair<Uri, String>> {
    // Create a mutable list to hold the result as pairs of (URI, type)
    val mediaList = mutableListOf<Pair<Uri, String>>()

    // Content URI that allows querying all types of media (files) from external storage
    val collection = MediaStore.Files.getContentUri("external")

    // Specify the columns we want to retrieve from the media database
    val projection = arrayOf(
        MediaStore.Files.FileColumns._ID,            // Unique ID for the media file
        MediaStore.Files.FileColumns.MEDIA_TYPE,     // Whether it's an image or video
        MediaStore.Files.FileColumns.RELATIVE_PATH   // Folder path (optional, useful for filtering)
    )

    // SQL-like WHERE clause: only return images or videos
    val selection = "${MediaStore.Files.FileColumns.MEDIA_TYPE}=? OR ${MediaStore.Files.FileColumns.MEDIA_TYPE}=?"
    val selectionArgs = arrayOf(
        MediaStore.Files.FileColumns.MEDIA_TYPE_IMAGE.toString(),
        MediaStore.Files.FileColumns.MEDIA_TYPE_VIDEO.toString()
    )

    // Sort results in descending order of date added — most recent first
    val sortOrder = "${MediaStore.Files.FileColumns.DATE_ADDED} DESC"

    // Execute the query on the content resolver using the specified parameters
    context.contentResolver.query(
        collection,
        projection,
        selection,
        selectionArgs,
        sortOrder
    )?.use { cursor -> // Use the cursor and auto-close it

        // Get the indices of the columns in the result set
        val idColumn = cursor.getColumnIndexOrThrow(MediaStore.Files.FileColumns._ID)
        val typeColumn = cursor.getColumnIndexOrThrow(MediaStore.Files.FileColumns.MEDIA_TYPE)
        val pathColumn = cursor.getColumnIndexOrThrow(MediaStore.Files.FileColumns.RELATIVE_PATH)

        // Iterate over each row in the result set
        while (cursor.moveToNext()) {
            val id = cursor.getLong(idColumn)           // Media file ID
            val type = cursor.getInt(typeColumn)        // Media type (image/video)
            val path = cursor.getString(pathColumn)     // Folder path (not currently used)

            // Build a URI based on the media type and ID
            val uri = when (type) {
                MediaStore.Files.FileColumns.MEDIA_TYPE_IMAGE ->
                    ContentUris.withAppendedId(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, id)

                MediaStore.Files.FileColumns.MEDIA_TYPE_VIDEO ->
                    ContentUris.withAppendedId(MediaStore.Video.Media.EXTERNAL_CONTENT_URI, id)

                else -> {
                    // Skip unsupported media types (e.g., audio, documents)
                    Log.e("MediaLoader", "Unsupported media type: $type for ID: $id")
                    continue
                }
            }

            // Convert type int to a readable string for your app logic
            val mediaType = if (type == MediaStore.Files.FileColumns.MEDIA_TYPE_IMAGE) "image" else "video"

            // Add the media item to the list as a Pair of (URI, type)
            mediaList.add(uri to mediaType)

            // Optional log for debugging: print the URI, type, and folder path
            Log.e("MediaLoader", "Loaded: $uri ($mediaType) in $path")
        }
    }

    // Log the total number of media items loaded
    Log.e("MediaLoader", "TOTAL: ${mediaList.size} items loaded")

    // Return the final list of image and video URIs with their type
    return mediaList
}

fun shareImagesOnWhatsApp(context: Context, uris: List<Uri>) {
    // Create an intent for sharing multiple images
    val intent = Intent().apply {
        action = Intent.ACTION_SEND_MULTIPLE // Allows sharing multiple files
        type = "image/*" // MIME type for images (WhatsApp will still accept videos if added)
        putParcelableArrayListExtra(Intent.EXTRA_STREAM, ArrayList(uris)) // URIs to share
        `package` = "com.whatsapp" // Target WhatsApp specifically
        addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION) // Grant read access to WhatsApp
    }

    try {
        // Show a chooser dialog to share the content
        context.startActivity(Intent.createChooser(intent, "Share via"))
    } catch (e: ActivityNotFoundException) {
        // Show a toast if WhatsApp is not installed
        Toast.makeText(context, "WhatsApp not installed", Toast.LENGTH_SHORT).show()
    }
}

@Composable
fun BottomBar(onHomeClick: () -> Unit, onShareClick: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth() // Stretch across the screen
            .background(Color.White) // White background for bar
            .padding(vertical = 10.dp, horizontal = 24.dp) // Inner padding
            .navigationBarsPadding(), // automatic bottom padding for nav bar
        horizontalArrangement = Arrangement.SpaceBetween, // Items at left and right
        verticalAlignment = Alignment.CenterVertically // Center icons/text vertically
    ) {
        // Share Text Button
        Text(
            text = "share",
            modifier = Modifier
                .clickable { onShareClick() } // Triggers share callback
                .background(Color.LightGray)
                .padding(8.dp),
            color = Color.DarkGray
        )

        // Home Icon Button
        Icon(
            imageVector = Icons.Default.Home,
            contentDescription = "Home",
            modifier = Modifier
                .size(28.dp)
                .clickable { onHomeClick() }, // Triggers home navigation callback
            tint = Color.Black
        )
    }
}

@Composable
fun ImagePreviewScreen(uri: Uri, onBack: () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxSize() // Take full screen
            .background(Color.Black), // Black background for better focus
        contentAlignment = Alignment.Center // Center image in the screen
    ) {
        Column(modifier = Modifier.fillMaxSize()) {

            //  Back Button at top-left (just like video screen)
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Default.ArrowBack,
                    contentDescription = "Back",
                    tint = Color.White,
                    modifier = Modifier
                        .size(30.dp)
                        .clickable { onBack() } // Back to gallery
                )
            }

            //  Image Viewer (fills the remaining space)
            Box(
                modifier = Modifier
                    .fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Image(
                    painter = rememberAsyncImagePainter(uri),
                    contentDescription = "Full image preview",
                    contentScale = ContentScale.Fit,
                    modifier = Modifier.fillMaxSize()

                )
            }
        }
    }
}


