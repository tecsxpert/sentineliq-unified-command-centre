package com.internship.tool.service;

//import com.internship.tool.entity.FileData;
//import com.internship.tool.repository.FileRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.util.UUID;

@Service
public class FileService {

//    private final FileRepository repo;

    @Value("${file.upload-dir}")
    private String uploadDir;

    public FileService() {
//        this.repo = repo;
    }

    public void uploadFile(MultipartFile file) throws Exception {

        String basePath = System.getProperty("user.dir");   // 🔥 project root

        File folder = new File(basePath + File.separator + "uploads");

        if (!folder.exists()) {
            folder.mkdirs();
        }

        String fileName = java.util.UUID.randomUUID() + "_" + file.getOriginalFilename();

        File dest = new File(folder, fileName);

        System.out.println("📍 Saving to: " + dest.getAbsolutePath());

        file.transferTo(dest);
    }

//   // public FileData getFile(Long id) {
//        return repo.findById(id).orElseThrow();
//    }
}
