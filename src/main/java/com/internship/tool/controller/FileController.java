package com.internship.tool.controller;

import com.internship.tool.entity.FileData;
import com.internship.tool.service.FileService;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import java.io.File;
import java.nio.file.Files;
import io.swagger.v3.oas.annotations.tags.Tag;
@Tag(name = "Files", description = "File upload/download APIs")

@RestController
public class FileController {

    private final FileService service;

    public FileController(FileService service) {
        this.service = service;
    }

    @Operation(summary = "Upload file")
    @ApiResponse(responseCode = "200", description = "File uploaded successfully")


    // 📤 Upload
    @PostMapping("/upload")
    public String upload(@RequestParam("file") MultipartFile file) throws Exception {
        //System.out.println("🔥 Upload API HIT");
        service.uploadFile(file);
        return "SUCCESS";
    }

    // 📥 Download
    @GetMapping("/files/{name}")
    public ResponseEntity<byte[]> download(@PathVariable String name) throws Exception {

        File file = new File("uploads/" + name);

        return ResponseEntity.ok()
                .body(java.nio.file.Files.readAllBytes(file.toPath()));
    }
}
